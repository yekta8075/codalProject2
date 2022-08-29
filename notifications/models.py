from django.db import models


class notification(models.Model):
    CompanyName = models.CharField(max_length=100)  # نام شرکت
    Symbol = models.CharField(max_length=100)  # نماد
    Title = models.CharField(max_length=1000)  # عنوان اطلاعیه
    LetterCode = models.CharField(max_length=20)  # کد
    SentDateTime = models.CharField(max_length=100)
    PublishDateTime = models.CharField(max_length=100)
    TracingNo = models.IntegerField(default=0)
    HasAttachment = models.BooleanField(default=False)
    HasHtml = models.BooleanField(default=False)
    HasXbrl = models.BooleanField(default=False)
    IsEstimate = models.BooleanField(default=False)
    Url = models.SlugField(max_length=200)  # مشاهده اطلاعیه
    PdfUrl = models.SlugField(max_length=200)
    ExcelUrl = models.SlugField(max_length=200)
    AttachmentUrl = models.SlugField(max_length=200)  # پیوست های اطلاعیه
    UnderSupervision = models.IntegerField(default=0)  # تحت احتیاط و مشمول فرآیند تعلیق
    HasExcel = models.BooleanField(default=False)
    HasPdf = models.BooleanField(default=False)
    XbrlUrl = models.SlugField(max_length=200)
    TedanUrl = models.SlugField(max_length=200)

    AdditionalInfo = models.CharField(max_length=1000, null=True)
    Reasons = models.CharField(max_length=1000, null=True)
    UnderSupervision1 = models.IntegerField(default=0)


class attachment(models.Model):
    AttachmentPath = models.CharField(max_length=1000)
    note = models.ForeignKey(notification, on_delete=models.CASCADE)

# def clear():
#     for table in reversed(db.metadata.sorted_tables):
#         db.engine.execute('TRUNCATE TABLE ' + table.name + ' RESTART IDENTITY CASCADE')
