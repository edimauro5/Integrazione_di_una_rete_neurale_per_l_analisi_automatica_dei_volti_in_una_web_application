import tensorflow as tf
import numpy as np

class SSD():
    i=0
    def __init__(self, model_filepath, inp_node_name='det%d/image_tensor', out_node_names=['det%d/detection_boxes', 'det%d/detection_scores', 'det%d/detection_classes']):
        with tf.compat.v2.io.gfile.GFile(model_filepath, 'rb') as f:
            graph_def = tf.compat.v1.GraphDef()
            graph_def.ParseFromString(f.read())
        self.sess = tf.compat.v1.Session(config=tf.compat.v1.ConfigProto(intra_op_parallelism_threads=1, inter_op_parallelism_threads=1))
        with self.sess.as_default():
            with self.sess.graph.as_default():
                name = 'det%d'%SSD.i
                tf.import_graph_def(graph_def,name=name)	
            #print('Ops:')
            #for o in tf.get_default_graph().as_graph_def().node:
            #	print(o.name)
            self.x = self.sess.graph.get_tensor_by_name((inp_node_name%SSD.i)+':0')
            print( "%s: input %s" % (name, str(self.x.shape)) )
            self.y = [self.sess.graph.get_tensor_by_name((out_node_name%SSD.i)+':0') for out_node_name in out_node_names]
        SSD.i+=1
        self.name = name
        self.n=0
    def det(self, img):
        self.n+=1
        LOGDIR = self.name
        NAME=self.name
        run_metadata = tf.compat.v1.RunMetadata()
        #writer  = tf.summary.FileWriter(LOGDIR + '/train/')
        run_options = tf.compat.v1.RunOptions(trace_level=tf.compat.v1.RunOptions.FULL_TRACE)
        with self.sess.as_default():
            boxes,scores,classes = self.sess.run(self.y, 
                        feed_dict={self.x: np.expand_dims(img, axis=0)},
                        options=run_options,
                        run_metadata=run_metadata
                        )
        
        #writer.add_run_metadata(run_metadata, NAME + "inference",self.n)
        #fetched_timeline = timeline.Timeline(run_metadata.step_stats)
        #chrome_trace = fetched_timeline.generate_chrome_trace_format()
        #with open(LOGDIR + '/timeline_{}.json'.format(self.n), 'w') as f:
        #    f.write(chrome_trace)


        return boxes,scores,classes