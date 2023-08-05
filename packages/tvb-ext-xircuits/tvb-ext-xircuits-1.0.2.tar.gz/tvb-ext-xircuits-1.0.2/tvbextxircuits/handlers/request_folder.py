from tqdm import tqdm
import os
from urllib import request, parse
from github import Github

from tvbextxircuits.logger.builder import get_logger

LOGGER = get_logger(__name__)


def request_folder(folder, repo_name="XpressAi/Xircuits", branch="master"):
    LOGGER.info("Downloading " + folder + " from " + repo_name + " branch " + branch)
    g = Github()
    
    try:
        repo = g.get_repo(repo_name)
        contents = repo.get_contents(folder, ref=branch)
    except:
       LOGGER.warn(folder + " from " + repo_name + " branch " + branch + " does not exist!")
       return 

    if not os.path.exists(folder):
        os.mkdir(folder)
    else:
        LOGGER.warn(folder + " already exists.")
    
    base_url = "https://raw.githubusercontent.com/" + repo_name + "/" + branch    
    urls = {}
    
    while len(contents)>0:
        file_content = contents.pop(0)
        if file_content.type=='dir':
            if not os.path.exists(file_content.path):
                os.mkdir(file_content.path)
            contents.extend(repo.get_contents(file_content.path, ref=branch))

        else:
            file_url = base_url + "/" + parse.quote(file_content.path)
            urls.update({file_url: file_content.path})

    for url in tqdm(urls):
        try:
            request.urlretrieve(url, urls[url])
        except:
            LOGGER.warn("Unable to retrieve " + urls[url] + ". Skipping...")