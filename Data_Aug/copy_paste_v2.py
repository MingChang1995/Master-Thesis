import cv2
import os
import random
import numpy as np
import xml.etree.ElementTree as ET
import xml.dom.minidom
import PIL.Image as img

def solve_coincide(box1,box2):
	x01, y01, x02, y02 = box1  
	x11, y11, x12, y12 = box2  
	col=max(0, min(x02,x12)-max(x01,x11))  
	row=max(0, min(y02,y12)-max(y01,y11))  
	intersection=col*row   
	return intersection 


img_path = './img/'         
xml_path = './xml/'          
img_names = os.listdir(img_path)
img_num = len(img_names)
print('img_num:', img_num)

count = 0
box_num = 0
potential_ins = ["button", "checkbox_checked", "checkbox_unchecked", "divider", "icon", "link", "logo", "scroll_bar", "text"]
potential_obj = potential_ins[0]
readlist = []
addlist = []

while count <= 400:
  i = random.randint(0, img_num-1)
  imgname = img_names[i]
  imgpath = img_path + imgname
  if imgpath not in readlist:
    im = img.open(imgpath)
    size = im.size
    img_w = size[0]
    img_h = size[1]
    print(img_h,img_w)

    j = random.randint(0, img_num-1)
    if i != j:
      add_path = img_path + img_names[j]
      if add_path not in addlist:
        addlist.append(add_path)
        readlist.append(imgpath)
        readlist.append(add_path)
        print("j:",j)
        addimg = img.open(add_path)
        add_w, add_h = addimg.size[0], addimg.size[1]
        count += 1
        print(count)
        print(add_h, add_w)
          

        if imgname == img_names[j]:
          print("The same image, no process!")

        else:
          xmlfile1 = xml_path + imgname[:-4] + '.xml'
          xmlfile2 = xml_path + img_names[j][:-4] + '.xml'
          print(xmlfile1,xmlfile2)

          tree1 = ET.parse(xmlfile1)
          tree2 = ET.parse(xmlfile2)
          root2 = tree2.getroot()

          objects1 = []
          bbox_2 = []
            
          for obj in tree1.findall("object"):
            obj_struct = {}
            obj_struct["name"] = obj.find("name").text
            obj_struct["pose"] = obj.find("pose")
            obj_struct["truncated"] = obj.find("truncated").text
            obj_struct["difficult"] = obj.find("difficult").text
            bbox = obj.find("bndbox")
            obj_struct["bbox"] = [float(bbox.find("xmin").text),
                                  float(bbox.find("ymin").text),
                                  float(bbox.find("xmax").text),
                                  float(bbox.find("ymax").text)]
            objects1.append(obj_struct)

          
          for obj in tree2.findall("object"):
            bbox = obj.find("bndbox")
            box = [float(bbox.find("xmin").text),
                  float(bbox.find("ymin").text),
                  float(bbox.find("xmax").text),
                  float(bbox.find("ymax").text)]
            bbox_2.append(box)


          paste_num = 0
          k = 0
          while paste_num <= 20 and k < len(objects1):
            ins = objects1[k]
	    box = ins["bbox"]
	    delta_x = box[2] - box[0]
	    delta_y = box[3] - box[1]
	    x1 = random.randint(0, add_w)
	    x2 = x1 + delta_x
	    y1 = random.randint(0, add_h)
	    y2 = y1 + delta_y
	    pos = [x1, y1, x2, y2]
	    if x2 < add_w and y2 < add_h and delta_x * delta_y > 10000:
              area = 0
              for o in bbox_2:
		s = solve_coincide(pos, o)
		area += s
              if area == 0:
		print("Big box: ")
		print(pos)
		bbox_2.append(pos)
		im_crop = im.crop((box[0],box[1],box[2],box[3]))
		addimg.paste(im_crop,(pos[0], pos[1]))
		addimg.save(add_path)
		newobject = ET.Element("object")
		newname = ET.Element("name")
		newname.text = ins["name"]
		newpose = ET.Element("pose")
		newpose.text = ins["truncated"]
		newtruncated = ET.Element("truncated")
		newtruncated.text = ins["truncated"]
		newDifficult = ET.Element("difficult")
		newDifficult.text = ins["difficult"]
		newbndbox = ET.Element("bndbox")
		newxmin = ET.Element("xmin")
		newxmin.text = str(pos[0])
		newymin = ET.Element("ymin")
		newymin.text = str(pos[1])
		newxmax = ET.Element("xmax")
		newxmax.text = str(pos[2])
		newymax = ET.Element("ymax")
		newymax.text = str(pos[3])
		newobject.append(newname)
		newobject.append(newpose)
		newobject.append(newtruncated)
		newobject.append(newDifficult)
		newobject.append(newbndbox)
		newbndbox.append(newxmin)
		newbndbox.append(newymin)
		newbndbox.append(newxmax)
		newbndbox.append(newymax)
		root2.append(newobject)
		tree2.write(xmlfile2)
		box_num += 1
		for l in range(len(objects1)):
		  sins = objects1[l]
		  if k != l:
		    box_in = sins["bbox"]
		    if box_in[0] >= box[0] and box_in[1] >= box[1] and box_in[2] <= box[2] and box_in[3] <= box[3]:
		      print("Inside box: ")
		        
		      ps_x1 = pos[0] + box_in[0] - box[0]
		      ps_y1 = pos[1] + box_in[1] - box[1]
		      ps_x2 = ps_x1 + box_in[2] - box_in[0]
		      ps_y2 = ps_y1 + box_in[3] - box_in[1]
		      print([ps_x1, ps_y1, ps_x2, ps_y2])

		      pasobject = ET.Element("object")
		      pasname = ET.Element("name")
		      pasname.text = sins["name"]
		      paspose = ET.Element("pose")
		      paspose.text = sins["truncated"]
		      pastruncated = ET.Element("truncated")
		      pastruncated.text = sins["truncated"]
		      pasDifficult = ET.Element("difficult")
		      pasDifficult.text = sins["difficult"]
		      pasbndbox = ET.Element("bndbox")
		      pasxmin = ET.Element("xmin")
		      pasxmin.text = str(ps_x1)
		      pasymin = ET.Element("ymin")
		      pasymin.text = str(ps_y1)
		      pasxmax = ET.Element("xmax")
		      pasxmax.text = str(ps_x2)
		      pasymax = ET.Element("ymax")
		      pasymax.text = str(ps_y2)
		      pasobject.append(pasname)
		      pasobject.append(paspose)
		      pasobject.append(pastruncated)
		      pasobject.append(pasDifficult)
		      pasobject.append(pasbndbox)
		      pasbndbox.append(pasxmin)
		      pasbndbox.append(pasymin)
		      pasbndbox.append(pasxmax)
		      pasbndbox.append(pasymax)
		      root2.append(pasobject)
		      tree2.write(xmlfile2)
		      box_num += 1
		paste_num += 1
	    k += 1


print(box_num)


