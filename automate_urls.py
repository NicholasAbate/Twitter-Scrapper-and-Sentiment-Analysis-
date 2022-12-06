with open('mid_handles.txt', 'r') as f:
    string = f.read()
    string.strip()
list = string.split('\n')
list.remove('')
urls = ['https://twitter.com']*len(list)
for i in range(len(list)):
    urls[i] += '/'+ list[i] + '/followers'
    print(urls[i])
