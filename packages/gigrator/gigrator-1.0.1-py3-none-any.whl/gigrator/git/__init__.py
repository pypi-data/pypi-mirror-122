"""
author: K8sCat <k8scat@gmail.com>
link: https://github.com/k8scat/gigrator.git
"""
import os

# 支持的Git服务器
SUPPORT_GITS = ['gitlab', 'github', 'gitee', 'gitea', 'coding', 'gogs', 'gf']

# 仓库暂存目录
TEMP_DIR = os.path.join(os.path.dirname(__file__), '.repos')

# GitLab
GITLAB_API_VERSION = '/api/v4'

# GitHub
# 暂不支持GitHub Enterprise
GITHUB_API = 'https://api.github.com/graphql'
GITHUB_SSH_PREFIX = 'git@github.com:'

# 码云
GITEE_API = 'https://gitee.com/api/v5'
GITEE_SSH_PREFIX = 'git@gitee.com:'

# Coding
# 暂不支持私有部署
CODING_SSH_PREFIX = 'git@e.coding.net:'

# Gitea/Gogs
GITEA_API_VERSION = '/api/v1'

# 腾讯工蜂
# 私有化部署请修改地址
GF_SSH_PREFIX = 'git@code.tencent.com'
GF_API = 'https://code.tencent.com/api/v3'
