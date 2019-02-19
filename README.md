# python
一、flac_download是flac格式歌曲下载软件，对于该代码，有以下注意点：
  1、本代码只可以下载flac格式的歌曲，其他格式的不能下载；
  2、UI使用Tkinter，界面美观性较差；
  3、可以使用python music.py来运行代码，也可以使用music.exe再win下运行，如果单独执行exe文件，需要把exe文件和conf.toml放在同一目录下；
  4、下载音乐是多任务完成的，要下载只需要双击歌曲名称；
  5、背景壁纸存放在image里面，更换壁纸只需要把新壁纸放到该文件，名称也要与原来的保持一致，大小必须是800*600；
  6、暂时不可以调整界面大小，因为没有解决背景图片自适应的bug；
  7、如果有任何问题，可以与我联系，sunhonx@outlook.com。
  8、该程序再win10——64下编写，只在该环境下测试；
  9、如果要运行该程序，他的依赖包请参考requirements.txt；