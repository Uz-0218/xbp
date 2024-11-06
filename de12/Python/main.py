name=input("名前を教えて下さい")
waist=input("腹囲は？")
age=input("年齢は？")


print(name, "さんは腹囲", waist, "cmで年齢は",age, "才ですね。")

if age<=25:
    print(name,"まだ遊んでいても大丈夫です")
else:
    print(name,"そろそろ結婚考えてもいい歳です")