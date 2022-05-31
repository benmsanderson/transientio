import pymrio
import country_converter as coco
import numpy as np
import matplotlib.pyplot as plt
import os

sav_path="/content/drive/MyDrive/pymrio"
raw_exio_path = '/tmp'

#download database
pymrio.download_exiobase3(  storage_folder=raw_exio_path,years=2010)

#parse database
wiod = pymrio.parse_exiobase3(raw_exio_path+'/IOT_2010_pxp.zip')

#print sectors in database
wiod.get_sectors()

#do aggregation
sectors=['food', 'mining', 'manufactoring', 'electricity', 'gas', 'construction', 'transport', 'other']



sec_agg_matrix=np.zeros([len(sectors),len(wiod.get_sectors())])

#Define sector ranges for each industry type
sec_agg_matrix[0,0:19]=1
sec_agg_matrix[1,20:41]=1
sec_agg_matrix[2,42:127]=1
sec_agg_matrix[3,128:141]=1
sec_agg_matrix[4,142:147]=1
sec_agg_matrix[5,148:156]=1
sec_agg_matrix[6,157:164]=1
sec_agg_matrix[7,165:199]=1

#aggregate regions and sectors
wiod_agg = wiod.aggregate(
    region_agg = coco.agg_conc(original_countries='EXIO3',
                               aggregates='continent',
                               missing_countries='Other',
                               merge_multiple_string=None),
                          sector_agg=sec_agg_matrix,
                          sector_names=sectors,
                                                     inplace=False)
#print aggrecated sectors
wiod_agg.get_regions()

wiod_agg.get_sectors()

#wiod_agg.Z

#Solve system
wiod_agg.calc_all()





os.chdir(r"/content/drive/MyDrive/pymrio")

save_folder_em= sav_path+'/emissions'
wiod_agg.impacts.save(path=save_folder_em)

save_folder_tr= sav_path+'/transition'
wiod_agg.save_all(path=save_folder_tr)
