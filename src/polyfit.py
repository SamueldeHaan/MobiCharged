import tensorflow as tf

# Create dataset
x_data = [[1], [2], [3], [4], [5]]
y_data = [[2], [4], [6], [8], [10]]

# Create variables for polynomial regression
W = tf.Variable(tf.random.normal(shape=[3, 1]))

# Create placeholders for input
x = tf.placeholder(dtype=tf.float32, shape=[None, 1])
y = tf.placeholder(dtype=tf.float32, shape=[None, 1])

# Create polynomial model
x_matrix = tf.concat([tf.pow(x, i) for i in range(3)], axis=1)
y_pred = tf.matmul(x_matrix, W)

# Create custom loss function
loss = tf.reduce_mean(tf.square(y - y_pred))

# Create optimizer
optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.01).minimize(loss)

# Initialize variables
init = tf.global_variables_initializer()

# Create session and run
with tf.Session() as sess:
    sess.run(init)
    for i in range(1000):
        _, curr_loss, curr_W = sess.run([optimizer, loss, W], feed_dict={x: x_data, y: y_data})
        if i % 100 == 0:
            print(f'Step {i}, Loss: {curr_loss}, W: {curr_W}')
    print(f'Final W: {curr_W}')