class Config:
    # 曲库数量限制
    limit: int = 3

    # 可选曲的白名单群组
    potato_group: int = 114514

    # 曲库储存路径
    ncm_pathway: str = 'data/potato_music_report/music.json'

    # 提醒时间
    ncm_notice_hour: int = 15
    ncm_notice_minute: int = 0

    # 广播时间
    ncm_broadcast_hour: int = 21
    ncm_broadcast_minute: int = 36

    # 单次会话超时时间，单位秒
    # nonebot 全局等待回复超时时间为120s
    timeout: int = 119

    # cd 时长，单位秒，用来给历史歌单冷却用
    cd: int = 30
