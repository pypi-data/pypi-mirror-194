"""
Tekton pipeline's data collector

"""
__version__="0.2.1"

from atlassian import Jira
import os
import re
import boto3
import json
import difflib
from bs4 import BeautifulSoup

class Collector:
    def __init__(self):
        jira_domain = os.getenv("JIRA_DOMAIN")
        jira_email = os.getenv("JIRA_EMAIL")
        jira_secret = os.getenv("JIRA_SECRET")

        self.region_name=os.getenv('AWS_REGION')
        self.aws_access_key_id=os.getenv('AWS_KEY_ID')
        self.aws_secret_access_key=os.getenv('AWS_KEY')

        self.jira = Jira(
            url=f'https://{jira_domain}',
            username=jira_email,
            password=jira_secret)
        
        self.cc = boto3.client(
            'codecommit',
            region_name=self.region_name,
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key
        )

        self.cr = boto3.client(
            'codeguru-reviewer',
            region_name=self.region_name,
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key
        )

    def from_tekton_pipelineruns(self, json_file_name: str):

        output = {}
        # Open the JSON file for reading
        with open(json_file_name, 'r') as file:
          # Load the contents of the file into a dictionary
          data = json.load(file)

        # Access the data in the dictionary
        uid = data.get('metadata')['uid']
        output['uid'] = uid
        output['tektonCreationTimestamp'] = data.get('metadata')['creationTimestamp']
        output['tektonGenerateName'] = data.get('metadata')['generateName']
        output['tektonName'] = data.get('metadata')['name']
        output['namespace'] = data.get('metadata')['namespace']
        output['tektonLastTransitionTime'] = data.get('status')['conditions'][0]['lastTransitionTime']

        params = {d['name']: d['value'] for d in data.get('spec')['params']}
        output.update(params)

        status_message = data.get('status')['conditions'][0]['message']
        print(status_message)

        # Extract the number of failed and cancelled tasks using regular expressions
        completed = re.search(r"Completed:\s*(\d+)", status_message)
        failed = re.search(r"Failed:\s*(\d+)", status_message)
        cancelled = re.search(r"Cancelled\s*(\d+)", status_message)

        # Convert the matched strings to integers or set to 0 if not found
        completed_count = int(completed.group(1)) if completed else 0
        failed_count = int(failed.group(1)) if failed else 0
        cancelled_count = int(cancelled.group(1)) if cancelled else 0

        output['tektonTaskCompletedCount'] = completed_count
        output['tektonTaskFailedCount'] = failed_count
        output['tektonTaskCancelCount'] = cancelled_count
        return output
    
    def from_testng(self, testng_path: str):
        results = {}
        results['testResultSkipped'] = "0"
        results['testResultfailed'] = "0"
        results['testResultIgnored'] = "0"
        results['testResultPassed'] = "0"
        results['testSuiteName'] = ""
        results['testDurationMs'] = ""
        results['testStartedAt'] = ""
        results['testFinishedAt'] = ""

        # check if a directory exists
        if os.path.isdir(testng_path) and os.path.isfile(f"{testng_path}/testng-results.xml"):
            with open(f"{testng_path}/testng-results.xml") as file:
                xml_str = file.read()
                
            soup = BeautifulSoup(xml_str, 'xml')
            results = {}
            testng = soup.find('testng-results')
            results['testResultSkipped'] = testng['skipped']
            results['testResultfailed'] = testng['failed']
            results['testResultIgnored'] = testng['ignored']
            results['testResultPassed'] = testng['passed']

            # Parse test suite information
            test_suite = soup.find('suite')
            results['testSuiteName'] = test_suite['name']
            results['testDurationMs'] = test_suite['duration-ms']
            results['testStartedAt'] = test_suite['started-at']
            results['testFinishedAt'] = test_suite['finished-at']

        return results
    
    def get_artifact_id(self, path_to_pom_file):
        if os.path.isdir(path_to_pom_file) and os.path.isfile(f"{path_to_pom_file}/pom.xml"):
            with open(f"{path_to_pom_file}/pom.xml") as file:
                xml_str = file.read()

                # Parse the XML string with BeautifulSoup
                soup = BeautifulSoup(xml_str, 'xml')

                # Find the artifactId element within the project element
                artifact_id = soup.select_one('project > artifactId')
                if artifact_id.text: 
                    return artifact_id.text
        
        return ""
    
    def from_jira(self, issue_key):
        if not issue_key:
            return {
                "jiraReporter" : "",
                "jiraCreatedDate": "",
                "jiraLastEditedDate": "",
                "jiraStatus": "",
                "jiraCommentNumber": "",
                "jiraCommentUniqueAuthor": ""
            }

        # retrieve the issue details
        issue = self.jira.issue(issue_key)

        # # get the reporter
        reporter = issue['fields']['reporter']['displayName']

        # get the last created date
        created_date = issue['fields']['created']

        # get the last edited date
        last_edited_date = issue['fields']['updated']

        # get the status
        status = issue['fields']['status']['name']

        # get the number of comments
        comments = self.jira.issue_get_comments(issue_key)
        num_comments = comments['total']

        # # get the number of unique authors in comments
        authors = set()
        for comment in comments['comments']:
            authors.add(comment['author']['displayName'])
        num_authors = len(authors)

        return {
            "jiraReporter" : reporter,
            "jiraCreatedDate": created_date,
            "jiraLastEditedDate": last_edited_date,
            "jiraStatus": status,
            "jiraCommentNumber": num_comments,
            "jiraCommentUniqueAuthor": num_authors
        }



    def get_code_diff(self, repository_name, after_commit_id, context=3):
        """
        Returns the code diff between two commit IDs in a CodeCommit repository.
        """
        print(repository_name)
        before_commit_id = self.get_commit_before(repository_name, after_commit_id)

        # Get the differences between the two commit IDs
        response = self.cc.get_differences(
            repositoryName=repository_name,
            beforeCommitSpecifier=before_commit_id,
            afterCommitSpecifier=after_commit_id
        )

        # Create a dictionary to store the file diffs
        file_diffs = {}

        # Loop through the differences and retrieve the contents of each file
        for difference in response['differences']:
            # Get the file path and type
            file_path = difference['afterBlob']['path']
            file_type = difference['afterBlob']['mode']

            # Get the contents of the before and after files
            before_blob_id = difference['beforeBlob']['blobId']
            before_blob = self.cc.get_blob(
                repositoryName=repository_name,
                blobId=before_blob_id
            )

            after_blob_id = difference['afterBlob']['blobId']
            after_blob = self.cc.get_blob(
                repositoryName=repository_name,
                blobId=after_blob_id
            )

            # Decode the contents of the before and after files
            before_content = before_blob['content'].decode('utf-8')
            after_content = after_blob['content'].decode('utf-8')

            # Generate a unified diff between the before and after content
            diff_lines = list(difflib.unified_diff(before_content.splitlines(), after_content.splitlines(), lineterm=''))

            # Truncate the unchanged context lines
            truncated_lines = []
            start_line = None
            for line_num, line in enumerate(diff_lines):
                if line.startswith('@@'):
                    start_line = None
                elif line.startswith('+') or line.startswith('-'):
                    if start_line is not None and line_num - start_line > context * 2:
                        truncated_lines.append('...')
                        start_line = None
                    truncated_lines.append(line)
                    start_line = line_num
                else:
                    if start_line is None:
                        truncated_lines.append(line)
                    elif line_num - start_line <= context:
                        truncated_lines.append(line)
                    elif start_line is not None and len(truncated_lines) > 0 and truncated_lines[-1] != '...':
                        truncated_lines.append('...')
                    start_line = None

            # Join the truncated lines into a string
            truncated_content = '\n'.join(truncated_lines)

            # Store the file diff in the dictionary
            file_diffs[file_path] = {
                'type': file_type,
                'before': before_content,
                'after': after_content,
                'diff': truncated_content
            }

        return file_diffs


    def get_commit_message(self, repo_name: str, commit_id: str):
        response = self.cc.get_commit(repositoryName=repo_name, commitId=commit_id)

        commit_msg = response['commit']['message']
        author = response['commit']['author']['email']
        jira_key = re.search(r'[A-Z-a-z-0-9]{2,4}-\d+', commit_msg)
        jira_key = jira_key.group(0) if jira_key else ""
        return {
            "jiraKey" : jira_key,
            "codeCommitMessage": commit_msg,
            "codeCommitAuthor": author
        }
    
    def get_commit_before(self, repository_name, commit_id):
        """
        Returns the commit ID before the specified commit ID in a CodeCommit repository.
        """
        # Get information about the specified commit
        response = self.cc.batch_get_commits(
            repositoryName=repository_name,
            commitIds=[commit_id]
        )

        if not response['commits']:
            # The specified commit ID was not found in the repository
            return None

        commit = response['commits'][0]

        if not commit['parents']:
            # The specified commit is the first commit in the repository
            return None

        # Get the ID of the parent commit
        previous_commit_id = commit['parents'][0]

        return previous_commit_id

    def count_file_changes(self, repository_name, after_commit_id):
        """
        Returns the number of file changes between two commit IDs in a CodeCommit repository.
        """
        before_commit_id = self.get_commit_before(repository_name, after_commit_id)
        
        # Get the differences between the two commit IDs
        response = self.cc.get_differences(
            repositoryName=repository_name,
            beforeCommitSpecifier=before_commit_id,
            afterCommitSpecifier=after_commit_id
        )
        
        # Count the number of file changes
        file_change_count = len(response['differences'])
        
        return file_change_count

    def get_codeguru_metrics(self, repository_name, commit_id):
        """
        Returns a list of CodeGuru suggestions for the given commit ID and repository.
        """
        # Get the latest CodeGuru code review ARN for the repository
        response = self.cr.list_code_reviews(
            Type="PullRequest",
            States=['Completed']
        )

        # Check if there are any code reviews for the repository
        if not response['CodeReviewSummaries']:
            print(f"No CodeGuru code reviews found for repository {repository_name}.")
            return []
        else:
            # Get the ARN of the latest code review
            code_review_arns = [review['CodeReviewArn'] for review in response['CodeReviewSummaries']]
            code_review_arn = [c for c in code_review_arns if commit_id in c]
            code_review_arn = code_review_arn[0] if code_review_arn else ""

            summary = [s for s in response['CodeReviewSummaries'] if s['CodeReviewArn'] == code_review_arn]
            summary = summary[0] if summary else {}
            
            if summary:
                return {
                    "codeGuruReviewArn": code_review_arn,
                    "codeGuruMeteredLinesOfCodeCount": summary['MetricsSummary']['MeteredLinesOfCodeCount'],
                    "codeGuruSuppressedLinesOfCodeCount": summary['MetricsSummary']['SuppressedLinesOfCodeCount'],
                    "codeGuruFindingsCount": summary['MetricsSummary']['FindingsCount'],
                    "codeGuruPullRequestId": summary['PullRequestId']
                }
            else:
                return {
                    "codeGuruReviewArn": code_review_arn,
                    "codeGuruMeteredLinesOfCodeCount": 0,
                    "codeGuruSuppressedLinesOfCodeCount": 0,
                    "codeGuruFindingsCount": 0,
                    "codeGuruPullRequestId": ""
                }
            