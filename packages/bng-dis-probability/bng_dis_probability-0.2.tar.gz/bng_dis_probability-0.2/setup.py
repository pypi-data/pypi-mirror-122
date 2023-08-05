from setuptools import setup

with open("C:/Users/hp/Desktop/LEARN/Udacity/python_gaussian_code/distributions_package/bng_dis_probability/README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(name='bng_dis_probability',
      version='0.2',
      description='Gaussian and Binomial distributions',
      long_description=long_description,
      long_description_content_type="text/markdown",
      packages=['bng_dis_probability'],
      author='Mohammed Hamza Malik',
      author_email='m.h.m.i.malik@gmail.com',
      zip_safe=False)
