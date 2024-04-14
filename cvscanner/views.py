from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import FileUploadForm
from .models import UploadedFile
from .script import process_files_in_zip, save_to_excel
from django.conf import settings
import os
import pandas as pd
from io import BytesIO


def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Process the uploaded file
            uploaded_file = request.FILES['file']
            file_instance = UploadedFile(file=uploaded_file)
            file_instance.save()  # Save the file to the media directory
            file_path = os.path.join(settings.MEDIA_ROOT, uploaded_file.name)
            data = process_files_in_zip(file_path)

            df = pd.DataFrame(data)
            excel_buffer = BytesIO()
            with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False)
            excel_buffer.seek(0)

            # Preparing response
            response = HttpResponse(excel_buffer.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="output.xlsx"'
            return response
    else:
        form = FileUploadForm()
    return render(request, 'index.html', {'form': form})