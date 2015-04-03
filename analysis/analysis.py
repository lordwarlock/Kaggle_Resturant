import re

class RestData(object):
    feat_dict = dict()
    def __init__(self,features,prediction):
        self.rest_id = int(features[0])
        self._update('id', self.rest_id)

        self.open_date = features[1]
        self._update('date', self.open_date)

        self.age = 2015 - int(features[1][-4:])
        self._update('age', self.age)

        self.city = features[2]
        self._update('city', self.city)

        self.city_group = re.sub(' ','_',features[3])
        self._update('city_group', self.city_group)

        self.rest_type = features[4]
        self._update('type', self.rest_type)

        self.p = [self.process_num(x) for x in features[5:]]
        [self._update('p'+str(i+1), self.p[i]) for i in range(37)]

        if prediction != []:
            self.prediction = float(prediction[0])
        else:
            self.prediction = 0

    def process_num(self,string):
        if '.' in string:
            return float(string)
        else:
            return string

    @classmethod
    def _update(cls,field,value):
        if field in cls.feat_dict:
            cls.feat_dict[field].add(value)
        else:
            cls.feat_dict[field] = set([value])

class DataAnalysis(object):
    def __init__(self,train_dir = '../train.csv',
                      test_dir = '../test.csv'):
        self.train_data = self.readRestData(train_dir)
        self.test_data = self.readRestData(test_dir)
        self.output_weka_arff(self.train_data)
        self.output_weka_arff(self.test_data,'../weka/test.arff',rel_name = 'test')

    def readRestData(self,file_dir):
        data = []
        with open(file_dir,'r') as f_i:
            _ = f_i.readline()
            for line in f_i:
                splitted = line[:-1].split(',')
                data.append(RestData(splitted[:42],splitted[42:]))
        return data
       
    def prediction_field_match(self,data,s1,s2):
        if s1==s2:
            return data.prediction
        else:
            return 0

    def output_matlab_csv(self,data_list,out_dir = '../matlab/train.csv'):
        with open(out_dir,'w') as f_o:
            for data in data_list:
                f_o.write(str(data.age)+',')
                f_o.write(str(int(data.city_group == 'Big Cities'))+',')
                f_o.write(str(int(data.rest_type == 'FC'))+',')
                p = [str(x) for x in data.p]
                f_o.write(','.join(p)+','+ str(data.prediction) +'\n')

    def output_weka_arff(self,data_list,out_dir = '../weka/train.arff',rel_name = 'train'):
        with open(out_dir,'w') as f_o:
            f_o.write(self._get_weka_header(rel_name))
            f_o.write(self._get_weka_body(data_list))

    def _get_weka_header(self,rel_name = 'train'):
        header_buffer = '@RELATION ' + rel_name + '\n\n'
        header_buffer += '@ATTRIBUTE\tage\tINTEGER\n'
        header_buffer += '@ATTRIBUTE\tcity_group\t{Big_Cities,Other}\n'
        header_buffer += '@ATTRIBUTE\ttype\t{DT,FC,IL,MB}\n'
        feat_len = len(self.train_data[0].p)
        for i in range(feat_len):
            if type(self.train_data[0].p[i]) == type('string'):
                #header_buffer += '@ATTRIBUTE\tp'+str(i+1)+'\t{'+','.join(self.train_data[0].feat_dict['p'+str(i+1)])+'}\n'
                header_buffer += '@ATTRIBUTE\tp'+str(i+1)+'\tINTEGER\n'
            else:
                header_buffer += '@ATTRIBUTE\tp'+str(i+1)+'\tREAL\n'

        header_buffer += '@ATTRIBUTE\trevenue\tREAL\n'
        header_buffer += '\n@DATA\n'
        return header_buffer

    def _get_weka_body(self,data_list):
        body_buffer = ''
        for data in data_list:
            body_buffer += str(data.age)+','
            body_buffer += data.city_group+','
            body_buffer += data.rest_type+','
            p = [str(x) for x in data.p]
            body_buffer += ','.join(p)
            body_buffer += ','+str(data.prediction)+'\n'
        return body_buffer

if __name__ == '__main__':
    DataAnalysis()
