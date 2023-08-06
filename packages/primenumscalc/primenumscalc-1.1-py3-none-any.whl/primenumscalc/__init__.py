from rpy2.robjects import r

def listPrimeNumbers(n):
    r_function = '''
    res <- c()
    if (N<=1) {
        cat("ERROR: Invalid input parameter. The value must be a natural number greater than 1")
        } else if (N==2) {
            res <- append(res,2) 
        } else if (N>2) {
            res <- append(res,2)
            for (i in 3:N)
            {   
                is_prime <- T
                for (j in 2:(i-1)) if(i%%j == 0) is_prime <- F 
                if (is_prime == T) res <- append(res, i)  
            }       
    }
    '''
    r.assign('N', n)
    r(r_function)
    result = r('res')
    return result



