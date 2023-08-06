from weibo_poster import Poster, WeiboRequest

poster = Poster(188888131, "e2ac9d62-bf44-4672-8cbb-2b420bc5cb0f", "https://api.nana7mi.link")
session = WeiboRequest("__bid_n=18533b242f69ae19a24207; FEID=v10-2a6b7672c6d14b3a63b660ff54ed7216958ad7d2; __xaf_fpstarttimer__=1671609598791; __xaf_thstime__=1671609599088; FPTOKEN=pNwOVh0jXd63LiE29ApxKk1wchwlbBotUcflHY3ONVOAs1s1ESAmSgMRUOJcaN77MYraiy6ABz15TcO8JS6BrA3krQpXVAxt8fb0suQInbGjRC0wbPy8+m1cko/J8IZwKJTGYRyAVU0Lz2PSV/HUqOooL9u5wtRbk/5YxMjtBvjGEgIJE33F2tpFt8ph6SjdonF/P0jlqGfUItbpCJNktIpgDsiVBGhhYtdsvwX8Ybdumo0plthtHLUNUzlCHEee3Q/HH0Lv/5LDQE4VXUFIygxQauGnspTj2XqolW4QLNVcJamqL57r9+wuW/fR09uLdcAxZkEdW4hOCisVCX5Ra1d1B45i+ool7RFtGDI79w0iXxlZog6W8stpPZZJFNZtoJ8ynRnxFUgimljhf5ErSOCncmmXo+UnIbLpNOU2lbXWKqpxssHRI4tmy3VjlZDo|/H4o3vcrKkl9fqduIT4uok7U1CbSQKJ0GLaja5QzWP4=|10|39c0b4c1947ce026e170cb5798a1c7a4; __xaf_fptokentimer__=1671609599153; _T_WM=9b632d4fa36e54f9746397f757d0abf8; SCF=Ape-KYlZqPHxNQ-dAyGy3Nr9b3Jrqq5WjQlhFqH6lZCVPjE1J1iePyeYNw4AkVfIQ0cE4bC_cinL_c_wp2vW7k4.; SUB=_2A25O6hLbDeRhGeFM7lQU8i7PyjmIHXVqFL6TrDV6PUJbktAGLU3_kW1NQNxRT0att90Nw7Goq8ABxn4sC_HsemVw; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWsM7qnLH5XXeUsRC8WX5b75JpX5K-hUgL.FoMESKqfeo50eK-2dJLoIpMLxKnL1hBL1hqLxK.LBozLBKnpeo2015tt; SSOLoginState=1676567179; ALF=1679159179; XSRF-TOKEN=5d71e1; WEIBOCN_FROM=1110006030; MLOGIN=1; mweibo_short_token=5ab04915c9; M_WEIBOCN_PARAMS=luicode=10000011&lfid=1076037198559139&fid=1005057198559139&uicode=10000011")
PostList = list()


@Poster.job(name="七海", start=2, args=["7198559139"])
@Poster.job(name="宁宁", start=4.5, args=["1765893783"])
async def weibo(uid: str):
    await poster.online()
    post = None
    async for post in session.posts(uid):
        if post.mid not in PostList:
            PostList.append(post.mid)
            await poster.update(post)
    if post is not None:
        async for comment in session.comments(post):
            if comment.uid == uid:
                await poster.update(comment)

Poster.run(Poster.stepBrother, poster)
