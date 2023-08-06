import sys
import os
import json
from github import Github
import urllib3

class PRLabel():
    def __init__(self, url=""):
        GIT_REPO_URL = r'https://github.customerlabs.com.au/api/v3'
        token = os.getenv("github_token")
        if token is None:
            print('Error','Not github connection token set in environment, exit')
            exit(1)
            
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        self.g = Github(base_url=GIT_REPO_URL, login_or_token=token, verify=False)
        url_ll = url.split("/")
        if len(url_ll) == 7: # https://github.customerlabs.com.au/sql-checkbot-test/iag-edh-data/pull/12
            self.repo_name, self.pr_number = url_ll[-4] + \
                "/" + url_ll[-3], int(url_ll[-1])
            print(f"inital label bot repo: {self.repo_name} PR:{self.pr_number}")
            self.repo = self.g.get_repo(self.repo_name)
            self.pr = self.repo.get_pull(self.pr_number)
        else:
            self.repo = None
            self.pr = None
            print('Error',f'PR is not in right format:{url}')
            exit (1)
            
        self.labels = self.get_label_list()

    def set_checkbot_status(self,name):
        self.set_label('checkbot', name)
        
    def set_project_type(self, name):
        name = self.pr.title()
        if not name.startswith("project"):
            name = "hotfix"
            
        self.set_label("project",name)
    
    def set_review(self,name):
        self.set_label("review",name)
                
    def set_intergation_status(self,name):
        self.set_label('intergation', name)
    
    def set_project(self):
        to_branch_full = self.pr.base.raw_data['label']
        from_branch_full = self.pr.head.raw_data['label']
        print(f"checking project from: {from_branch_full} to:{to_branch_full}")
        lb = "hotfix"
        if 'project_' in to_branch_full:
            lb = to_branch_full.split(":")[1]
        if 'project_' in from_branch_full:
            lb = from_branch_full.split(":")[1]
        self.pr.add_to_labels(lb)
        print(f'added label: {lb}')        
            
    def set_size(self):
        changes = self.pr.raw_data['additions'] + self.pr.raw_data['deletions'] + self.pr.raw_data['changed_files']
        _size = 'XS'
        if changes > 1000:
            _size = 'XXL'
        elif changes > 500:
            _size = 'XL'
        elif changes > 100:
            _size = 'L'
        elif changes > 30:
            _size = 'M'
        elif changes > 10:
            _size = 'S' 
        else:
            _size = 'XS' 
        self.set_label("size", _size)
                                                   
    def set_label(self, type, name):
        try:
            n,c,d = self.labels[type][name].split("|")
        except:
            print(f'{type},{name} not found')
            return
                    
        if self.labels[type]["replace"]:
            for lb in self.pr.get_labels() :
                print(f'current label: {lb.name}  {lb.color}  {lb.description}')
                # finds = set(self.pr_labels).intersection(self.labels[type])
                # for lb in finds:
                if lb.name.startswith(type):
                    if lb.name != n:
                        print(f'remove label: {lb.name}, replace with {n}')
                        self.pr.remove_from_labels(lb.name)
                    else : 
                        print(f'same label: {lb.name} == {n}')        
                        return
        self.label_exists(n,c,d)
        self.pr.add_to_labels(n)
        print(f'added label: {n} {c} {d}')
        
    def add_pr_reviewers(self, pr_reviewers):
        self.pr.create_review_request(pr_reviewers)

    def get_reviewers(self):
        return self.pr.get_reviews()

    def label_exists(self,n,c,d):
        for lb in self.repo.get_labels():
            if lb.name == n :
                if lb.color == c and lb.description == d:
                    print(f'found label {n}')
                    return 
                else:
                    print(f'need modify label:{lb.color}!={c} {lb.description} !={d}')
        
        print(f'create label name: {n}, color: {c}, desc: {d}')
        try:
            self.repo.create_label(n,c,d)
        except Exception as e :
            print(f'Error to create label name: {n}, color: {c}, desc: {d}\n {e}')

    def create_issue_comment(self, cm):
        self.pr.create_issue_comment(cm)
        
    def get_label_list(self):
        with open ('./github_pr_label/labels.json','r') as f:
            return json.load(f)

## assigned, closed
if __name__ == "__main__":
    pr_url, type, name = sys.argv[1],sys.argv[2],sys.argv[3]
    # pr_url = "https://github.customerlabs.com.au/s106916/github-action-test/pull/2"
    # t = "https://github.customerlabs.com.au/iagcl/iag-edh-ci-testing/pull/640"
    bot = PRLabel(pr_url)
    bot.set_size()
    bot.set_project()
    if name != 'unknown':
        bot.set_label(type,name)
