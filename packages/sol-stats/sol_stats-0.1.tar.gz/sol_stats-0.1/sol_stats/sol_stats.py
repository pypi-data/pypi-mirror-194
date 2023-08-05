

x=[0]

class stats:
    def mean(x):
        i=0
        total=0
        while(i<+len(x)):
            total= total+x[i]
            i=i+1
        m=total/len(x)
        print("The total of list =",total)
        print("The mean of list =",m)
    # mean(x)

    def median(x):
        a=0
        list.sort(x)
        a=len(x)/2
        b=int(a)
        if a!=b:
            md=x[b]
        else:
            md=(x[b]+x[b+1])/2

        print("The number of element in list=",len(x))
        print("The median of list =",md)
        # print(b)
    # median(x)

    def mod(x):
        a=max(set(x), key=x.count)
        print("The mod of the list =",a)
    # mod(x)
