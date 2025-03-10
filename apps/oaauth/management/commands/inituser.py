from django.core.management.base import BaseCommand
from apps.oaauth.models import OAUser, OADepartment


class Command(BaseCommand):
    def handle(self, *args, **options):
        boarder = OADepartment.objects.get(name="董事会")
        developer = OADepartment.objects.get(name="产品开发部")
        operator = OADepartment.objects.get(name="运营部")
        saler = OADepartment.objects.get(name="销售部")
        hr = OADepartment.objects.get(name="人事部")
        finance = OADepartment.objects.get(name="财务部")

        # 董事会的员工，都是superuser用户
        # 1. 赵磊：属于董事会的leader
        zhaolei = OAUser.objects.create_superuser(
            email="zhaolei@qq.com",
            realname="赵磊",
            password="111111",
            department=boarder,
        )
        # 2. 王磊：董事会
        wanglei = OAUser.objects.create_superuser(
            email="wanglei@qq.com",
            realname="王磊",
            password="111111",
            department=boarder,
        )
        # 3. 李明：产品开发部leader
        liming = OAUser.objects.create_user(
            email="liming@qq.com",
            realname="李明",
            password="111111",
            department=developer,
        )
        # 4. 张三：运营部leader
        zhangsan = OAUser.objects.create_user(
            email="zhangsan@qq.com",
            realname="张三",
            password="111111",
            department=operator,
        )
        # 5. 王航：人事部leader
        wanghang = OAUser.objects.create_user(
            email="wanghang@qq.com", realname="王航", password="111111", department=hr
        )
        # 6. 赵亮：财务部leader
        zhaoliang = OAUser.objects.create_user(
            email="zhaoliang@qq.com",
            realname="赵亮",
            password="111111",
            department=finance,
        )
        # 7. 孙华：销售部 leader
        sunhua = OAUser.objects.create_user(
            email="sunhua@qq.com", realname="孙华", password="111111", department=saler
        )

        # 给部门指定leader和manager
        # 分管的部门
        # 赵磊：产品开发部、运营部、销售部
        # 王磊：人事部、财务部
        # 1. 董事会
        boarder.leader = zhaolei
        boarder.manager = None

        # 2. 产品开发部
        developer.leader = liming
        developer.manager = zhaolei

        # 3. 运营部
        operator.leader = zhangsan
        operator.manager = zhaolei

        # 4. 销售部
        saler.leader = sunhua
        saler.manager = zhaolei

        # 5. 人事部
        hr.leader = wanghang
        hr.manager = wanglei

        # 6. 财务部
        finance.leader = zhaoliang
        finance.manager = wanglei

        boarder.save()
        developer.save()
        operator.save()
        saler.save()
        hr.save()
        finance.save()

        self.stdout.write("初始用户创建成功")
