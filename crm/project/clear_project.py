from project.models import *

### cleaning comments
pc = projectcomment.objects.all()
for c in pc:
	if c.projectstep_set.count() or c.project_set.count():
		print(c,"has project or projectstep")
	else:
		print(c,"will be deleted")
		c.delete()

#### cleaning pictures
pictures = projectpict.objects.all()
for p in pictures:
	if p.projectcomment_set.count() or p.projectstep_set.count() or p.project_set.count():
		print(p,"has projectcomment or project or projectstep")
	else:
		print(p,"will be deleted")
		p.delete()

#### cleaning pictures
files = projectfile.objects.all()
for f in files:
	if f.projectcomment_set.count() or f.projectstep_set.count() or f.project_set.count():
		print(f,"has projectcomment or project or projectstep")
	else:
		print(f,"will be deleted")
		f.delete()

	
