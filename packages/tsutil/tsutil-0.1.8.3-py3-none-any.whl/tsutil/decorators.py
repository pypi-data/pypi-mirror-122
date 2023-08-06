# -*- coding: utf-8 -*-
from functools import wraps
from typing import Optional, Union
from concurrent import futures

def singleton(cls, *args, **kwargs):
  '''
  singleton decorator
  '''
  instances = {}

  def _singleton():
    if cls not in instances:
      instances[cls] = cls(*args, **kwargs)
    return instances[cls]
  return _singleton

def singleton_fun(fun):
  '''
  对方法的返回结果做单例
  使用参数作为key
  '''
  instances = {}
  @wraps(fun)
  def _singleton(*args, **kwargs):
    k = fun.__name__ + '_' + '|'.join(map(lambda it: str(it), args)) + '_' + '|'.join(str(it[0])+str(it[1]) for it in tuple(kwargs))
    if k not in instances:
      instances[k] = fun(*args, **kwargs)
    return instances[k]
  return _singleton


class timeout:
  '''为函数设置一个超时时间，当超时时会抛出concurrent.futures._base.TimeoutError'''
  __excutor = futures.ThreadPoolExecutor(1)
  seconds: Optional[float] = None
  
  def __init__(self, seconds: Union[float]):
    self.seconds = seconds

  def __call__(self, func):
    @wraps(func)
    def wrapper(*args, **kwargs):
      future = self.__excutor.submit(func, *args, **kwargs)
      return future.result(timeout=self.seconds)
    return wrapper

class allow_count:
  def __init__(self, count: Union[int]):
    self.count = count
    self.cur = 0
  
  def __call__(self, func):
    @wraps(func)
    def wrapper(*args, **kwargs):
      if self.cur >= self.count:
        return
      
      self.cur += 1
      return func(*args, **kwargs)
    return wrapper
