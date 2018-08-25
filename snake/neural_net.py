'''
DeepLearning Snake
Copyright (C) 2018 by Antonio J. Grandson Busson <busson@outlook.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
'''

import tensorflow as tf
from snake import *


tf_sess = None
tf.set_random_seed(0)

def create_neural_network_1(num_features, num_output):

    #camada de entrada (x)
    x = tf.placeholder(dtype=tf.float32, shape=[None, num_features])

    #label
    y = tf.placeholder(dtype=tf.float32, shape=[None, num_output])

    #camada escondida 1 (sigmoid)
    hidden_layer1 = tf.layers.dense(x, num_features, activation=tf.nn.sigmoid)

    #camada escondida 2 (sigmoid)
    hidden_layer2 = tf.layers.dense(hidden_layer1, 2, activation=tf.nn.sigmoid)

    #camada de saida (linear)
    out_layer = tf.layers.dense(hidden_layer2, num_output, activation=None)

    cost = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits=out_layer, labels=y))

    #Optimizer
    opt = tf.train.AdamOptimizer(learning_rate=0.01).minimize(cost)

    out = tf.nn.sigmoid(out_layer)

    return x, y, out, cost, opt


def init_tensorflow():
    global tf_sess
    tf_sess.run(tf.global_variables_initializer())

def create_neural_net(mode):
    global tf_sess
    if tf_sess == None:
        tf_sess = tf.InteractiveSession()

    if mode == "hungry":
        x, y, out, cost, opt = create_neural_network_1(5,2)
    else:
        x, y, out, cost, opt = create_neural_network_1(4,1) 

    neural_net = {"x": x,"y": y, "output": out, "cost": cost, "opt":opt}
    return neural_net
    
   
def feed_neural_net(snake, x_data, y_data, in_train_mode):
    
    model = snake["neural_net"]

    x = model["x"]
    y = model["y"]
    out = model["output"]
    cost = model["cost"]
    opt = model["opt"]

   
    _, loss, dec = tf_sess.run([opt,cost,out], feed_dict={x: x_data, y: y_data})
   
    if snake["mode"] == "hungry":
        dec = np.sum(dec, axis=1)

    #print("perda:",loss, "esquerda:", dec[0], "adiante", dec[1], "direta:", dec[2])
   
    arg_max = np.argmax(dec)
    if arg_max == 0:
        return -1
    elif arg_max == 1:
        return 0
    elif arg_max == 2:
        return 1
    

        

   

    
