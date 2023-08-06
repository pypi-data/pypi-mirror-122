import logging

import torch
from torchvision.models import resnet18
import torch.nn as nn
import indexedconv.utils as cvutils
from indexedconv.engine import IndexedConv, IndexedMaxPool2d
from gammalearn.utils import get_camera_layout_from_geom


class GLNetIndexConv42(nn.Module):
    """
        Network with indexed convolutions and pooling.
        4 CL (after each conv layer, pooling is executed)
        2 FC
    """
    def __init__(self, net_parameters_dic, camera_geometry, mode='train'):
        """
        Parameters
        ----------
        net_parameters_dic (dict): a dictionary describing the parameters of the network
        camera_parameters (dict): a dictionary containing the parameters of the camera used with this network
        mode (str): explicit mode to use the network (different from the nn.Module.train() or evaluate()). For GANs
        """
        super(GLNetIndexConv42, self).__init__()
        self.logger = logging.getLogger(__name__ + '.GLNetIndexConv42')
        self.targets = net_parameters_dic['targets']

        index_matrix1, camera_layout = get_camera_layout_from_geom(camera_geometry)
        pooling_kernel = camera_layout

        # Channels
        num_outputs = sum(net_parameters_dic['targets'].values())
        self.num_channel = n1 = net_parameters_dic['num_channels']
        n_features = net_parameters_dic['n_features']
        n2 = n_features*2
        n3 = n2*2
        n4 = n3 * 2

        self.drop_rate = net_parameters_dic['drop_rate']

        # Layer 1 : IndexedConv
        indices_conv1 = cvutils.neighbours_extraction(index_matrix1,
                                                      kernel_type=camera_layout)
        # After the first convolution we need to reorganize the index matrix
        index_matrix1 = cvutils.pool_index_matrix(index_matrix1, kernel_type=pooling_kernel, stride=1)
        indices_pool1 = cvutils.neighbours_extraction(index_matrix1, kernel_type=pooling_kernel, stride=2)
        self.cv1 = IndexedConv(n1, n_features, indices_conv1)
        self.max_pool1 = IndexedMaxPool2d(indices_pool1)
        self.relu1 = nn.ReLU()
        self.bn1 = nn.BatchNorm1d(n_features)

        # Layer 2 : IndexedConv
        index_matrix2 = cvutils.pool_index_matrix(index_matrix1, kernel_type=pooling_kernel, stride=2)
        indices_conv2 = cvutils.neighbours_extraction(index_matrix2,
                                                      kernel_type=camera_layout)
        indices_pool2 = cvutils.neighbours_extraction(index_matrix2, kernel_type=pooling_kernel, stride=2)
        self.cv2 = IndexedConv(n_features, n2, indices_conv2)
        self.max_pool2 = IndexedMaxPool2d(indices_pool2)
        self.relu2 = nn.ReLU()
        self.bn2 = nn.BatchNorm1d(n2)

        # Layer 3 : IndexedConv
        index_matrix3 = cvutils.pool_index_matrix(index_matrix2, kernel_type=pooling_kernel, stride=2)
        indices_conv3 = cvutils.neighbours_extraction(index_matrix3,
                                                      kernel_type=camera_layout)
        indices_pool3 = cvutils.neighbours_extraction(index_matrix3, kernel_type=pooling_kernel, stride=2)
        self.cv3 = IndexedConv(n2, n3, indices_conv3)
        self.max_pool3 = IndexedMaxPool2d(indices_pool3)
        self.relu3 = nn.ReLU()
        self.bn3 = nn.BatchNorm1d(n3)

        # Layer 4 : IndexedConv
        index_matrix4 = cvutils.pool_index_matrix(index_matrix3, kernel_type=pooling_kernel, stride=2)
        indices_conv4 = cvutils.neighbours_extraction(index_matrix4,
                                                      kernel_type=camera_layout)
        indices_pool4 = cvutils.neighbours_extraction(index_matrix4, kernel_type=pooling_kernel, stride=2)
        self.cv4 = IndexedConv(n3, n4, indices_conv4)
        self.max_pool4 = IndexedMaxPool2d(indices_pool4)
        self.relu4 = nn.ReLU()
        self.bn4 = nn.BatchNorm1d(n4)

        index_matrix5 = cvutils.pool_index_matrix(index_matrix4, kernel_type=pooling_kernel, stride=2)

        # Compute the number of pixels (where idx is not -1 in the index matrix) of the last features
        n_pixels = int(torch.sum(torch.ge(index_matrix5[0, 0], 0)).data)
        self.logger.debug('num pixels after last conv : {}'.format(n_pixels))

        self.lin1 = nn.Linear(n_pixels*n4, (n_pixels*n4) // 2)
        self.relu5 = nn.ReLU()
        self.bn5 = nn.BatchNorm1d((n_pixels*n4) // 2)

        self.lin2 = nn.Linear((n_pixels*n4)//2, num_outputs)

        for m in self.modules():
            if isinstance(m, IndexedConv):
                nn.init.kaiming_uniform_(m.weight.data, mode='fan_out')

    def forward(self, x):
        drop = nn.Dropout(p=self.drop_rate)
        out_conv = []
        # In case of stereo, average convolutions output per telescope
        for i in range(int(x.shape[-2] / self.num_channel)):
            out = self.cv1(x[..., i*self.num_channel:(i+1)*self.num_channel, :])
            out = self.max_pool1(out)
            out = self.bn1(out)
            out = drop(self.relu1(out))
            out = self.cv2(out)
            out = self.max_pool2(out)
            out = self.bn2(out)
            out = drop(self.relu2(out))
            out = self.cv3(out)
            out = self.max_pool3(out)
            out = self.bn3(out)
            out = drop(self.relu3(out))
            out = self.cv4(out)
            out = self.max_pool4(out)
            out = self.bn4(out)
            out_conv.append(drop(self.relu4(out)))
        out = torch.stack(out_conv, 1)
        out = out.mean(1)
        out = out.view(out.size(0), -1)
        out = self.lin1(out)
        out = self.bn5(out)
        out = drop(self.relu5(out))

        out_linear2 = self.lin2(out)
        i = 0
        output = {}
        for t, v in self.targets.items():
            if t == 'class':
                output[t] = nn.LogSoftmax(1)(out_linear2[:, i:i + v])
            else:
                output[t] = out_linear2[:, i:i+v]
            i += v

        return output


class ResNet18MT(nn.Module):
    """
        ResNet18 for multitask IACT reco
    """
    def __init__(self, net_parameters_dic, camera_geometry):
        """
        Parameters
        ----------
        net_parameters_dic (dict): a dictionary describing the parameters of the network
        camera_parameters (dict): a dictionary containing the parameters of the camera used with this network
        mode (str): explicit mode to use the network (different from the nn.Module.train() or evaluate()). For GANs
        """
        super(ResNet18MT, self).__init__()
        self.logger = logging.getLogger(__name__ + '.ResNet18MT')
        self.targets = net_parameters_dic['targets']

        self.model = resnet18(pretrained=False)

        # Channels
        num_outputs = sum(net_parameters_dic['targets'].values())
        num_channel = net_parameters_dic['num_channels']
        self.model.conv1 = torch.nn.Conv2d(num_channel, 64, kernel_size=(3, 3), padding=(1, 1))
        self.drop_rate = net_parameters_dic['drop_rate']
        self.model.fc = nn.Linear(512, 256)
        self.relu5 = nn.ReLU()
        self.bn5 = nn.BatchNorm1d(256)
        self.lin2 = nn.Linear(256, num_outputs)

        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                nn.init.kaiming_uniform_(m.weight.data, mode='fan_out')

    def forward(self, x):
        drop = nn.Dropout(p=self.drop_rate)
        out = self.model(x)
        out = self.bn5(out)
        out = drop(self.relu5(out))

        out_linear2 = self.lin2(out)
        i = 0
        output = {}
        for t, v in self.targets.items():
            if t == 'class':
                output[t] = nn.LogSoftmax(1)(out_linear2[:, i:i + v])
            else:
                output[t] = out_linear2[:, i:i+v]
            i += v

        return output
