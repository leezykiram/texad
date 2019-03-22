import csv
import json
import os
import sys

from django.conf import settings


def convert_csv_to_json(input_fn, output_fn):
    """
    Arguments:
    input_fn - Input CSV filename
    output_fn - Output JSON filename
    
    Returns:
    JSON convered filename
    """
    

    ifp = open(input_fn, 'r')
    ofp = open(output_fn, 'w')

    fieldnames = ('id', 'description', 'datetime', 'longitude', 'latitude', 'elevation')
    reader = csv.DictReader(ifp, fieldnames) 
    data = [row for row in reader if row]
    try:
        assert sorted(data[:1][0].values()) == sorted(list(fieldnames))
    except AssertionError:
        print ("CSV headers {} did match as expected {}".format(data[:1][0].values(),fieldnames))
        print ("Exiting the program with exit status -1")
        sys.exit(-1)

    # convert it into the way we want:
    data = data[1:]
    output = []
    for d in data:
        output_dict=dict(product={})
        output_dict['product']=dict(product_id=d['id'],description=d['description'])
        output_dict['track_datetime']=d['datetime']
        output_dict['longitude']=d['longitude']
        output_dict['latitude']=d['latitude']
        output_dict['elevation']=d['elevation']
        output.append(output_dict.copy())        
    print("There were {} rows in the csv".format(len(output)))
    data = sorted(output)
    json.dump(data, ofp,indent=4,sort_keys=True)
    print("Wrote to {} file".format(output_fn))
    
    ofp.close()
    ifp.close()

    return output_fn


if __name__ == "__main__":
    # TODO use settings
    dir_name = '/home/ramki/Documents/gigs/texada_software/aircraft_tracker/light_jets/sample_data'
    input_file = os.path.join(dir_name,'initial_data.csv')
    output_file = os.path.join(dir_name,'initial_data.json')
    convert_csv_to_json(input_file,output_file)
