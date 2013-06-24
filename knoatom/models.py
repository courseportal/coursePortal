from django.db import models

#bugReport
class BugReport(models.Model):
	subject = models.CharField(max_length=100)
	content = models.TextField()
	email = models.EmailField()
	cc_myself = models.BooleanField(default=False)
	def __unicode__(self):
		return self.subject
	class Meta:
		ordering = ['subject']
		verbose_name_plural = "BugReports"