'''
Created on Oct 2, 2014

@author: jiayu.zhou
'''


import numpy as np;

class ProxOptimizer(object):
    
    FLAG_OPTIM   = 1;
    FLAG_XTOL    = 2;
    FLAG_FTOL    = 3;
    FLAG_MAXITER = 4;
    FLAG_MAXFEV  = 5;
    FLAG_OTHER   = 6;
  
    MESSAGE_OPTIM   = 'Optimality below optim_tol.';
    MESSAGE_XTOL    = 'Relative change in x below xtol.';
    MESSAGE_FTOL    = 'Relative change in function value below ftol.';
    MESSAGE_MAXITER = 'Max iterations reached.';
    MESSAGE_MAXFEV  = 'Max function evaluations reached.';
    

def proximal(f, prox_f):
    '''
    construct a proximal operand used for proximal methods, e.g. sparsa. 
    prox_f( y, t ) = argmin_X 1/(2*t)*|| x - y ||^2 + f(x)
                   = argmin_X 1/2 *|| x - y ||^2 + t * f(x)
                   
    e.g. to solve l1 norm. 
         f(x)         = lam * np.norm(x,'fro');
         prox_f(x, t) = np.multiply(x, (1 - np.minimum( (t * lamb)/abs(x), 1 )));
    '''
    
    def fcn_impl(x, t = None):
        if t is not None: # if step length exists, perform projection.
            x = prox_f(x, t);
        v = f(x);
        return [v, x];
    
    return fcn_impl;



def prox_l1(lamb):
    '''
    The proximal function of l1 norm regularization.
    The function is constructed from proximal(f, prox_f).
    
    Parameters
    ----------
    lamb: the l1 regularization.   
    '''
    # function value.
    gx    = lambda x : lamb * np.linalg.norm(x, 1);
    # proximal gradient. 
    # prox_f( y, t ) = argmin_X 1/(2*t)*|| x - y ||^2 + lamb * |x|
    gprox = lambda x, t :  np.multiply(x, (1 - np.minimum( (t * lamb)/abs(x), 1 )));
    # construct proximal methods.  
    return proximal(gx, gprox);

def projfun_probability_simplex(v, lamb):
    # check if the vector is column vector.
    
    # work.
    if isinstance(v, np.matrix):
        if not v.shape[1] == 1:
            raise ValueError('the variable to be projected should be a column vector.');
        if v.shape[0] == 1:
            return np.matrix(lamb);
        
        v = np.multiply(v > 0, v);
        #u = np.sort(v)[::-1, ::-1];   # sort and reverse.
        u = np.sort(v, axis = 0)[::-1];   # sort and reverse. 
        sv = np.cumsum(u).T;
        srt = (sv - lamb)/ (np.matrix(range(v.shape[0])) + 1).T;
        
        rho = np.max(np.nonzero(u > srt)[0]) + 1 # find.
        theta = np.max([0, (sv[rho - 1] - lamb) / rho]);
        xx = np.maximum(v - theta, 0);
        return xx;
    elif isinstance(v, np.ndarray):
        if len(v.shape)>1:
            raise ValueError('the variable to be projected should be 1d ndarray.');
        if v.shape[0] == 1:
            return np.array([lamb]);
        
        v = np.multiply(v > 0, v);
        u = np.sort(v)[::-1];   # sort and reverse. 
        sv = np.cumsum(u).T;
        srt = (sv - lamb)/ (np.array(range(v.shape[0])) + 1);
        
        rho = np.max(np.nonzero(u > srt)[0]) + 1 # find.
        theta = np.max([0, (sv[rho - 1] - lamb) / rho]);
        xx = np.maximum(v - theta, 0);
        return xx;
    else:
        raise ValueError('unsupported projection type.')

def proj_nonneg_simplex(lamb):
    '''
    Projection to the non-negative simplex
    
    Parameters
    ----------
    lamb: the 
    '''
    gx     = lambda x    : 0;
    gprox  = lambda x, t : projfun_probability_simplex(x, lamb);
    # construct proximal methods. 
    return proximal(gx, gprox);

def proj_nonneg():
    '''
    Projection to the non-negative half-space. 
    '''
    gx     = lambda x    : 0;
    gprox  = lambda x, t : np.multiply(x > 0, x);
    # construct proximal methods. 
    return proximal(gx, gprox);

if __name__ == '__main__':
    print 'test proj_nonneg_simplex(lamb)'
    simplex_projector = proj_nonneg_simplex(1);
    
    v = [2.81472368639318, 2.90579193707562, 2.12698681629351, 2.91337585613902, 2.63235924622541, \
         2.09754040499941, 2.27849821886705, 2.54688151920498, 2.95750683543430, 2.96488853519928]
    print '------np.ndarray-----'
    
    varr = np.array(v);
    print 'Original ndarray vector:'
    print varr;
    print 'Projected ndarray vector:'
    print projfun_probability_simplex(varr, 1);
    
    
    print '------np.matrix------' 
    v = np.matrix(v).T - 2.5;
    print 'Original matrix vector:'
    print v.T;
    
    [_, pv] = simplex_projector(v, 0);
    print 'Projected matrix vector:'
    print pv.T;
    
    print 'Sum:' 
    print np.sum(pv);
    
    
    print 'non-negative half-space projection'
    v = [2.81472368639318, 2.90579193707562, 2.12698681629351, 2.91337585613902, 2.63235924622541, \
         2.09754040499941, 2.27849821886705, 2.54688151920498, 2.95750683543430, 2.96488853519928]
    nneg_projector = proj_nonneg();
    print '------np.matrix------' 
    v = np.matrix(v).T - 2.5;
    print 'Original matrix vector:'
    print v.T;
    
    [_, pv] = nneg_projector(v, 0);
    print 'Projected matrix vector:'
    print pv.T;
    
    
    
    pass;

    