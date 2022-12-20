import glob
import pandas as pd
import random

extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]

random.shuffle(all_filenames)

trainfiles = all_filenames[:3]
testfiles = all_filenames[3:5]

print(trainfiles)
print(testfiles)

#combine all files in the list
train_csv = pd.concat([pd.read_csv(f) for f in trainfiles])
#export to csv
train_csv.to_csv( "s3_train3_csv.csv", index=False, encoding='utf-8-sig')


#combine all files in the list
test_csv = pd.concat([pd.read_csv(f) for f in testfiles])
#export to csv
test_csv.to_csv( "s3_test2_csv.csv", index=False, encoding='utf-8-sig')