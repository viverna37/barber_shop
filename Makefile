REPO = 'git@github.com:viverna37/barber_shop.git'
BRANCH = master




git_work:
	git init
	git add .
	git commit -m "new commit"
	git push $(REPO) $(BRANCH)
