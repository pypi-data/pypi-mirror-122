Waifu-Pypics
==========

Python Wrapper for `Waifu-Pics <https://waifu.pics>`_ Api

Installing
----------

To install this library use the command:

.. code:: sh

    pip install waifu-pypics





Sync Example
~~~~~~~~~~~~~

.. code:: py

    from waifu_pypics import Waifu
    
    
    waifu = Waifu()
    
    
    print(waifu.get_image('hug'))



Async Example
--------------

.. code:: py

    import asyncio

    from waifu_pypics import WaifuAsync
    
    
    waifu = WaifuAsync()
    

    if __name__ == "__main__":
      loop = asyncio.get_event_loop()
      loop.run_until_complete(waifu.get_image('hug'))
      loop.close()

