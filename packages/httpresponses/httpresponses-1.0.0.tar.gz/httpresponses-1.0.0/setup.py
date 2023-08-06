import setuptools

with open("README.md", "r", encoding = "utf-8") as descfile: desc = descfile.read()
setuptools.setup(name = "httpresponses", version = "1.0.0", author = "Fasm.ga", author_email = "developers@fasmga.org", description = "A really simple module to help you with HTTP responses", long_description = desc, long_description_content_type = "text/markdown", url = "https://github.com/fasm-ga/httpresponses", project_urls = { "Bug Tracker": "https://github.com/fasm-ga/httpresponses/issues", }, classifiers = [ "Programming Language :: Python :: 3", "License :: OSI Approved :: MIT License", "Operating System :: OS Independent", ], package_dir = { "": "src" }, packages = setuptools.find_packages(where = "src"))
