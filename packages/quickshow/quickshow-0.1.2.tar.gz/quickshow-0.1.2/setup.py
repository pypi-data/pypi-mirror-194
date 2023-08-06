# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['quickshow']

package_data = \
{'': ['*'], 'quickshow': ['output/*']}

install_requires = \
['matplotlib>=3.7.0,<4.0.0',
 'pandas>=1.5.3,<2.0.0',
 'scikit-learn>=1.2.1,<2.0.0',
 'seaborn>=0.12.2,<0.13.0',
 'sklearn>=0.0.post1,<0.1']

setup_kwargs = {
    'name': 'quickshow',
    'version': '0.1.2',
    'description': '',
    'long_description': '# Quick-Show\n- Quick-Show is a package that allows you to easily and quickly draw 2D or 3D t-SNE and PCA plots using specific columns of a refined dataframe.\n- Quick Show is an abstraction using popular libraries such as sklearn and matplotlib, so it is very light and convenient.\n- `Note`: quich show is sub-modules of other packages to manage quickshow more lightly and use more widly.\n- 추가 업데이트 계획이 있으므로, 간단한 함수로 관리하며, 추가 배포 예정 레포의 서브 모듈로 사용함.\n<br>\n\n## Quick Start\n  ```cmd\n  $ pip install quickshow\n  ```\n- Create a scatter plot very quickly and easily by inputting a clean dataframe and column names that do not have missing data. \n- If the label column does not exist, simply enter `None` as an argument.\n  ```python\n  from quickshow import vis_tsne2d, vis_tsne3d, vis_pca\n\n  # Make sample df\n  df = pd.DataFrame([3,2,3,2,3,3,1,1])\n  df[\'val\'] = [np.array([np.random.randint(0,10000),np.random.randint(0,10000),np.random.randint(0,10000)]) for x in df[0]]\n  df.columns = [\'labels\', \'values\']\n\n  # Use matplotlib rcparams or returned dataframe for customize your plot.\n  return_df = vis_tsne2d(df, \'values\', \'labels\', False, \'fig1.png\')\n  return_df = vis_tsne3d(df, \'values\', \'labels\', False, \'fig2.png\')\n  return_df = vis_pca(df, \'values\', \'labels\', 2, False, \'fig3.png\')\n  return_df = vis_pca(df, \'values\', \'labels\', 3, False, \'fig4.png\')\n  ```\n\n  <img src="https://github.com/DSDanielPark/quick-show/blob/main/quickshow/output/readme_fig1.png" width="500"><BR>\n  <img src="https://github.com/DSDanielPark/quick-show/blob/main/quickshow/output/readme_fig2.png" width="500"><BR>\n  - For more details, please check doc string.\n<br>\n<br>\n\n\n## Functions\nIt contains 3 functions: `vis_tsne2d`, `vis_tsne3d`, `vis_pca`\n- (1) `vis_tsne2d` function: Simple visuallization of 2-dimensional t-distributed stochastic neighbor embedding\n- (2) `vis_tsne3d` function: Simple visuallization of 3-dimensional t-distributed stochastic neighbor embedding\n- (3) `vis_pca` function: Simple visuallization of Principal Component Analysis (PCA)\n\n\nAll function returns the dataframe which used to plot. Thus, use the returned dataframe object to customize your plot. Or use [matplotlib\'s rcparam](https://matplotlib.org/stable/tutorials/introductory/customizing.html) methods.\n<br>\n<br>\n\n\n## References\n[1] sklearn.manifold.TSNE https://scikit-learn.org/stable/modules/generated/sklearn.manifold.TSNE.html <br>\n[2] sklearn.decomposition.PCA https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html <br>\n[3] matplotlib https://matplotlib.org/\n',
    'author': 'parkminwoo',
    'author_email': 'parkminwoo1991@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
