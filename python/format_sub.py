__author__ = 'sleep'


if __name__ == '__main__':
    with open("../prediction","r") as f_pre:
        with open("../pre_format.txt","w") as f_write:
            f_write.write("Id,Prediction\n")
            for line in f_pre:
                if line == '\n': continue
                preline = line.split()
                if preline[0].startswith("in"):
                    continue

                else:
                    id = preline[0]
                    id = int(id) - 1
                    pre = float(preline[2])
                    to_write = str(id) + "," + str(pre)
                    f_write.write(to_write)
                    f_write.write("\n")


