import xml.dom.minidom
import os
import requests
import urllib
from urllib.parse import urlparse
from urllib.request import urlretrieve



from dao.DaoClass import DaoClass


def download_syllabus(url,name, code, description, directory="../syllabuses"):
    if not os.path.exists(directory):
        os.makedirs(directory)
    filename = f"{name}-{code}-{description.replace(' ', '-')}.pdf"
    file_path = os.path.join(directory, filename)

    try:
        urllib.request.urlretrieve(url, file_path)
        print(f"Syllabus guardado en: {file_path}")
    except Exception as e:
        print(f"Error al descargar el syllabus desde {url}: {e}")




domtree = xml.dom.minidom.parse("files/courses.xml")
courses = domtree.getElementsByTagName("Courses")
daoCourses = DaoClass()
for course in courses:
        classes = course.getElementsByTagName("classes")[0]
        code = classes.getElementsByTagName('code')[0].childNodes[0].nodeValue
        name = classes.getElementsByTagName('name')[0].childNodes[0].nodeValue

        cid = course.getElementsByTagName('classid')[0].childNodes[0].nodeValue
        cred = course.getElementsByTagName('cred')[0].childNodes[0].nodeValue
        description = course.getElementsByTagName('description')[0].childNodes[0].nodeValue
        syllabus = course.getElementsByTagName('syllabus')[0].childNodes[0].nodeValue
        term = course.getElementsByTagName('term')[0].childNodes[0].nodeValue
        years= course.getElementsByTagName('years')[0].childNodes[0].nodeValue

        course_info = (cid, name, code, description, term, years, cred, syllabus)
        # daoCourses.insertCourse(course_info)
        daoCourses.insertCourse(course_info)

        #download_syllabus(syllabus, name ,code,description)

daoCourses.closeConnection()






