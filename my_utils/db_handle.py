from google.cloud import firestore, storage
import requests
from google.cloud.firestore import FieldFilter as fil
import time
import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile
import os

class DBHandle:
  def __init__(self, dbname) -> None:
    self.dbName = dbname

    # Sử dụng credentials từ Streamlit secrets
    import firebase_admin
    from firebase_admin import credentials, firestore, storage

    # Kiểm tra xem Firebase app đã được khởi tạo chưa
    try:
      firebase_admin.get_app()
    except ValueError:
      # Lấy credentials từ Streamlit secrets
      if 'firebase' in st.secrets:
          # Convert secrets dict to proper credential format
          cred_dict = dict(st.secrets['firebase'])
          cred = credentials.Certificate(cred_dict)
      else:
          # Fallback to local file for development
          cred = credentials.Certificate('hchuong-firebase-adminsdk-1m82k-a70c60ad91.json')
      firebase_admin.initialize_app(cred)

    self.db = firestore.client()
    self.bucket = storage.bucket("hchuong.appspot.com")

  def insert(self, data: dict):
    try:
      new_ref = self.db.collection(self.dbName).add(data)
      new_reff = new_ref[0]
      print('Time insert:', new_ref[0].to_datetime())
      return new_ref[1].id
    except Exception as e:
      print(f"Error inserting data: {str(e)}")
      return False

  def update(self, id, data: dict):
    try:
      return self.db.collection(self.dbName).document(id).update(data)
    except Exception as e:
      print(f"Error updating data: {str(e)}")
      return False

  def get_all(self):
    try:
      return self.db.collection(self.dbName).stream()
    except Exception as e:
      print(f"Error getting all data: {str(e)}")
      return False

  def get_by_id(self, id):
    try:
      return self.db.collection(self.dbName).document(id).get()
    except Exception as e:
      print(f"Error getting data by ID: {str(e)}")
      return False

  def delete(self, id):
    try:
      return self.db.collection(self.dbName).document(id).delete()
    except Exception as e:
      print(f"Error deleting data: {str(e)}")
      return False      
  
  def upload_file(self, file: UploadedFile, path: str):
    try:
      # Tạo tên file với đường dẫn đầy đủ
      file_path = f"{path}/{file.name}"
      
      # Upload file
      blob = self.bucket.blob(file_path)
      blob.upload_from_file(file, content_type=file.type)
      return True
    except Exception as e:
      print(f"Error uploading file: {str(e)}")
      return False
