venv-create:
	python3 -m venv virtualenv

venv-activate:
	source virtualenv/bin/activate

venv-lock:
	./virtualenv/bin/pip3 freeze > requirements.txt

venv-install-all:
	./virtualenv/bin/pip3 install -r requirements.txt

venv-install:
	./virtualenv/bin/pip3 install $(package)

ansible-deploy:
	ansible-playbook -i $$HOME/.ansible/inventory ./ansible/deploy.yaml

ansible-remove:
	ansible-playbook -i $$HOME/.ansible/inventory ./ansible/remove.yaml

git:
	git add . && git commit -m "$(msg)" && git push origin master

git-deploy: git ansible-deploy

api:
	./virtualenv/bin/python3 ./src/api.py