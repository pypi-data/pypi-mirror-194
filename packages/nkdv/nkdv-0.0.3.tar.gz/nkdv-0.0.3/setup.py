from setuptools import setup, find_packages   

# with open("README.md") as f:
#     long_description = f.read()
    

setup(
    name = "nkdv",
    version = "0.0.3",
    keywords = ["pip", "KDE","heatmap","KDV","KeplerGL"],
    description = "A library of feature heatmap algorithm",
    #long_description= long_description,
    #long_description_content_type='text/markdown',
    license = "MIT Licence",

    url = "https://github.com/edisonchan2013928/Network-K-function",  
    author = "Tsz Nam Chan,PakLon Ip, Ryan Leong Hou U",
    author_email = "paklonip@um.edu.mo",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",     
)