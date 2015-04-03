import glob
import re
from subprocess import call

class WekaProcess():

    def weka_regression(self,
                        algorithm = 'weka.classifiers.meta.Bagging',
                        train_dir = '/Users/Zheng/Documents/IndStd/taste/class_weka_data/1_*train.arff',
                        out_dir = '/Users/Zheng/Documents/IndStd/taste/result/',
                        options = []):
        file_list = glob.glob(train_dir)
        for f_train in file_list:
            f_test = re.sub('train','test',f_train)
            f_name = self.get_file_name(f_train)
            print f_name,f_test
            f_name = re.sub('train','test',f_name)
            f_log = open(out_dir+'log_'+f_name,'w')
            f_res = open(out_dir+f_name,'w')
            for i in range(100):
                print i
                call(['java','-classpath','$CLASSPATH:weka.jar']
                     + [algorithm] + ['-c','last','-s',str(i),
                      '-t',f_train,'-x','5'] + options,stdout = f_log)
            #for i in range(100,1,-1):
            #    print i
            #    call(['java','-classpath','$CLASSPATH:weka.jar']
            #         + [algorithm] + [str(i),'-c','last',
            #          '-t',f_train,'-T',f_test,'-p','0'] + options,stdout = f_res)
                
            f_res.close()


    def get_file_name(self,string):
        match = re.match('.*/([0-9]+.*arff)',string)
        return match.group(1)

    def batch_process_given_algorithm(self,
                      start_no = 1,
                      out_num = 4,
                      algorithm = 'weka.classifiers.meta.Bagging',
                      train_dir = '/Users/Zheng/Documents/IndStd/taste/class_weka_data/',
                      out_dir = '/Users/Zheng/Documents/IndStd/taste/result/',
                      options = []):
        call(['rm','-r',out_dir])
        call(['mkdir',out_dir])
        for i in range(start_no,out_num):
            print 'output',i
            train_files = train_dir + '{0}_*train.arff'.format(str(i))
            self.weka_regression(algorithm,
                                 train_files,
                                 out_dir,options)

if __name__ == '__main__':
    import sys
    if len(sys.argv) == 0:
        WekaProcess().batch_process_given_algorithm(
            algorithm = 'weka.classifiers.meta.Bagging',
            train_dir = '/Users/Zheng/Documents/IndStd/taste/class_weka_data/',
            out_dir = '/Users/Zheng/Documents/IndStd/taste/result/')
    elif len(sys.argv) == 3:
        WekaProcess().batch_process_given_algorithm(
            algorithm = 'weka.classifiers.meta.Bagging',
            train_dir = sys.argv[1],
            out_dir =  sys.argv[2])
    elif len(sys.argv) == 4:
        WekaProcess().batch_process_given_algorithm(
            algorithm = sys.argv[3],
            train_dir = sys.argv[1],
            out_dir =  sys.argv[2])
    elif len(sys.argv) > 4:
        print 4
        WekaProcess().batch_process_given_algorithm(
            algorithm = sys.argv[3],
            train_dir = sys.argv[1],
            out_dir =  sys.argv[2],
            options = sys.argv[4:])
    else:
        print '[train-dir] [out-dir] [algorithm]'
        print '[train-dir] /Users/Name/Documents/IndStd/taste/class_weka_data/'
        print '[out-dir]   /Users/Name/Documents/IndStd/taste/result/'
        print '[algorithm] weka.classifiers.meta.Bagging'
        print "python ../taste/weka_regression.py /home/g/grad/zhihaozh/Documents/taste/class_weka_data/ /home/g/grad/zhihaozh/Documents/taste/bagging_result/"
    
