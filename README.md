class_info.csv 此檔案是我自己對Google open image V5整理出各類別的所有訓練影像數量，其中數量包含是每個類別(train+test+validation)的影像數量，可以給您做參考。<br/>

Google_openData_precess.py 此程式針對 [Google open image V5](https://storage.googleapis.com/openimages/web/download.html "Title")下載後的數據，使用「類別名稱」進行數據選取，挑出想要訓練的類別數據。<br/>

使用 Google_openData_precess.py 程式時，我的資料結構如下，train、test、validation目錄存放影像集，<br/>
**{類別名稱}_DataSet** 目錄是執行一次成後會產生的目錄:<br/>

    Google_Open_ImageV5/
        ---csv/
           -class_info.csv
           -class-descriptions-boxable.csv
           -train-annotations-bbox.csv
           -test-annotations-bbox.csv
           -validation-annotations-bbox.csv
        ---train_00/
        ---train_01/
        ---train_02/
        ---train_03/
        ---train_04/
        ---train_05/
        ---train_06/
        ---train_07/
        ---train_08/
        ---test/
        ---validation/
        ---{類別名稱}_DataSet/
        
執行 Google_openData_precess.py 必須定義清楚自己的資料路徑以及變數，則路徑建議使用「絕對路徑」，避免不必要的錯誤發生<br/>

    Example:
    cvs_path = 'Google_Open_ImageV5/csv'
    image_path = 'Google_Open_ImageV5/'
    output_path = 'Google_Open_ImageV5/'
    select_class_name = '{輸入想要選取的類別英文名稱，務必完整符合class_info.csv或class-descriptions-boxable.csv之英文名稱}'
    
image_process_tensorflow.py 此程式針對「擁有標籤檔案(**.xml**)」的影像數據集，在使用[Tensorflow Object Detection API](https://github.com/tensorflow/models "Title")訓練前的數據前處理。<br/>

使用 image_process_tensorflow.py 程式時，我的資料結構如下:<br/>
**Output_DataSet/** 目錄是執行一次成後會產生的目錄:<br/>

    Google_Open_ImageV5/
        ---csv/
        ---train_00/
        ---train_01/
        ---train_02/
        ---train_03/
        ---train_04/
        ---train_05/
        ---train_06/
        ---train_07/
        ---train_08/
        ---test/
        ---validation/
        ---Hat_DataSet/
        ---Dog_DataSet/
        ---{Output_DataSet/}
           ---data/
               -train_labels.csv
               -train.record
               -validation_labels.csv
               -validation.record
            -object_detection.pbtxt
            ---train/
            ---test/
            ---validation/

執行 image_process_tensorflow.py 必須定義清楚自己的資料路徑以及變數，則路徑建議使用「絕對路徑」，避免不必要的錯誤發生<br/>

    Example:
    input_path = 'Google_Open_ImageV5/'
    output_path = 'Google_Open_ImageV5/Output_DataSet/'
    DataSet_Folder = ['Hat_DataSet','Dog_DataSet']
    split_rate = [0.94, 0.04, 0.02]
    
完成後，請依照Tensorflow Object Detection API 所需數據進行建置
