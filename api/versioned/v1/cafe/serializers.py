from rest_framework import serializers
import datetime
from api.bases.cafe.models import Cafe, Thumbnail, Menu


class ThumbnailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thumbnail
        fields = '__all__'


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'


class CafeSerializer(serializers.ModelSerializer):
    menu_info = serializers.CharField(write_only=True)
    thumUrls = serializers.ListField(child=serializers.URLField(), write_only=True)
    business_hours = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Cafe
        fields = (
            'menu_info', 'thumUrls', 'cafe_id', 'title', 'address', 'road_address',
            'latitude', 'longitude', 'tel', 'home_page', 'business_hours'
        )

    def to_internal_value(self, data):
        business_hours = data.pop('business_hours')
        start_time_str, end_time_str = business_hours.split('~')
        start_time = datetime.datetime.strptime(start_time_str.strip(), '%Y%m%d%H%M')
        end_time = datetime.datetime.strptime(end_time_str.strip(), '%Y%m%d%H%M')
        data['business_hours_start'] = start_time
        data['business_hours_end'] = end_time
        data = super().to_internal_value(data=data)
        return data

    def create(self, validated_data):
        menu_info = validated_data.pop('menu_info')
        thum_urls = validated_data.pop('thumUrls')

        # Cafe 모델 인스턴스를 생성하거나 업데이트합니다.
        cafe, created = Cafe.objects.update_or_create(
            cafe_id=validated_data.get('cafe_id'),
            title=validated_data.get('title'),
            defaults=validated_data
        )

        # Menu 모델 인스턴스를 찾아서 해당 인스턴스를 업데이트합니다.
        menus = cafe.menu_set.all()
        existing_menu_names = [menu.name for menu in menus]
        incoming_menu_infos = menu_info.split(' | ')
        incoming_menu_names = [menu_info.rsplit(' ', 1)[0] for menu_info in incoming_menu_infos]
        for menu in menus:
            if menu.name not in incoming_menu_names:
                menu.delete()

        for menu_info in incoming_menu_infos:
            name, price = menu_info.rsplit(' ', 1)[0], menu_info.rsplit(' ', 1)[1]
            if name in existing_menu_names:
                menu = Menu.objects.get(cafe=cafe, name=name)
                menu.price = int(price.replace(',', ''))
                menu.save()
            else:
                Menu.objects.create(cafe=cafe, name=name, price=int(price.replace(',', '')))

        # Thumbnail 모델 인스턴스를 생성하거나 업데이트합니다.
        existing_thumbnail_urls = [thumbnail.url for thumbnail in cafe.thumbnail_set.all()]
        for url in thum_urls:
            if url not in existing_thumbnail_urls:
                Thumbnail.objects.create(cafe=cafe, url=url)

        return cafe


