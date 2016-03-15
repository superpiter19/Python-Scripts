import urllib

sHost = "http://3.bp.blogspot.com/-UI5TbCquXn4/UHMvjf5vtJI/AAAAAAAABcM/69yqh0jNu8c/s1600/imgalbert%252Beinstein2.jpeg&w=640&h=625&ei=i2QLUfynNOmn0AXXpYGYCQ&zoom=1"
sDownloadPath = "D:\\ejemplosPython\\file.jpg"

urllib.urlretrieve(sHost,sDownloadPath)
