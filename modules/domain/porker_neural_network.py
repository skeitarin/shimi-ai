import os, sys, argparse
from os import path
import numpy as np
import tensorflow as tf
from sklearn.cross_validation import train_test_split

FLAGS = None
ckpt_path = "modules/domain/model/model_poker.ckpt"

def main(_):
    #スクリプトのあるディレクトリの絶対パスを取得
    name = os.path.dirname(os.path.abspath(__name__)) 
    #絶対パスと相対パスをくっつける
    joined_path = os.path.join(name, 'modules/domain/data/porker.csv')
    #正規化して絶対パスにする
    data_path = os.path.normpath(joined_path)

    # import data
    data = np.loadtxt(data_path, delimiter=',').astype(np.float32)
    # 入力値 データレイアウト
    # [1枚目の柄, 1枚目の数　・・・　5枚目の柄, 5枚目の数]
    #  柄→1：スペード、2：クローバー、3：ダイヤ、4：ハート
    x_data = data[:,0:10]  
    # 入力値 データレイアウト
    # [役]
    #  役→0：約無し、　・・・　9：ロイヤルストレートフラッシュ
    t_data = data[:,10:11].astype(np.int)
    t_data = np.eye(10)[t_data.flatten()] # one-hotに変換
    
    # 訓練データと検証データに分割
    x_train, x_test, t_train, t_test = train_test_split(x_data, t_data, test_size=0.2, random_state=1234)
    
    # define model
    x = tf.placeholder(tf.float32, [None, 10])
    y = interface(x)

    # define loss and optimizer
    y_ = tf.placeholder(tf.float32, [None, 10])
    cross_entropy = -tf.reduce_sum(y_*tf.log(y))
    train_step = tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy)
    
    # 保存の準備
    saver = tf.train.Saver()

    sess = tf.InteractiveSession()
    tf.global_variables_initializer().run()

    correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    # train
    for step in range(30001):
        batch_mask = np.random.choice(x_train.shape[0], 100)
        x_batch = x_train[batch_mask]
        t_batch = t_train[batch_mask]

        sess.run(train_step, feed_dict={x: x_batch, y_: t_batch})
        if step % 1000 == 0:
            train_accuracy = accuracy.eval({x: x_test, y_: t_test})
            print('test accuracy : ', train_accuracy)
            # print('accuracy : ', sess.run(accuracy, feed_dict={x: x_test, y_: t_test}))
    
    # test trained model
    correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    print('accuracy : ', sess.run(accuracy, feed_dict={x: x_test, y_: t_test}))
    
    # 最終的なモデルを保存
    save_path = saver.save(sess, ckpt_path)

def interface(x_placeholder):
    hdn_neuron = 80

    x = x_placeholder
    W1 = tf.Variable(tf.random_normal([10, hdn_neuron], mean=0.0, stddev=1.0))
    b1 = tf.Variable(tf.zeros([hdn_neuron]))
    l1 = tf.sigmoid(tf.matmul(x, W1) + b1)

    W2 = tf.Variable(tf.random_normal([hdn_neuron, hdn_neuron], mean=0.0, stddev=1.0))
    b2 = tf.Variable(tf.zeros([hdn_neuron]))
    l2 = tf.sigmoid(tf.matmul(l1, W2) + b2)

    W3 = tf.Variable(tf.random_normal([hdn_neuron, hdn_neuron], mean=0.0, stddev=1.0))
    b3 = tf.Variable(tf.zeros([hdn_neuron]))
    l3 = tf.sigmoid(tf.matmul(l2, W3) + b3)

    # W4 = tf.Variable(tf.random_normal([hdn_neuron, hdn_neuron], mean=0.0, stddev=1.0))
    # b4 = tf.Variable(tf.zeros([hdn_neuron]))
    # l4 = tf.sigmoid(tf.matmul(l3, W4) + b4)

    Wl = tf.Variable(tf.random_normal([hdn_neuron, 10], mean=0.0, stddev=1.0))
    bl = tf.Variable(tf.zeros([10]))
    y = tf.nn.softmax(tf.matmul(l3, Wl) + bl)
    return y

def predict(param):
    tf.reset_default_graph()
    
    logits = interface(param)

    sess = tf.InteractiveSession()
    # restore(パラメーター読み込み)の準備
    saver = tf.train.Saver()
    tf.global_variables_initializer().run()
    # 学習語モデルを読み込み
    saver = tf.train.import_meta_graph(ckpt_path + ".meta") # 追加
    saver.restore(sess, ckpt_path)

    softmax = logits.eval()
    result = softmax[0]
    rates = [round(n * 100.0, 1) for n in result]
    return rates
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_dir', type=str, default='/tmp/tensorflow/mnist/input_data',
                      help='Directory for storing input data')
    FLAGS, unparsed = parser.parse_known_args()
    tf.app.run(main=main, argv=[sys.argv[0]] + unparsed)

