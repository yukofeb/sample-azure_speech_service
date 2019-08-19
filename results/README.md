# ソースコード
以下を参考にした  
[cognitive\-services\-speech\-sdk/samples/batch/python at master · Azure\-Samples/cognitive\-services\-speech\-sdk](https://github.com/Azure-Samples/cognitive-services-speech-sdk/tree/master/samples/batch/python)  

# 結果
# sample01
## 音源特徴
* 男性と女性の会話  
* かなりカジュアルな語り口&会話がかぶっている箇所もあるので、識別難易度はかなり高そう  
* ソース  
https://pj.ninjal.ac.jp/corpus_center/csj/sample.html の 課題指向対話音声  

## 解析結果
[result01.txt](results01.txt)  

## 所感
* 精度は悪いが、これはデータが難しすぎた（GCPでもボロボロだった）  

# sample02（話者識別あり）
## 音源特徴
* 男性が一人で話している（講演会？）  
* 割とはっきりとした口調  
* ソース  
https://pj.ninjal.ac.jp/corpus_center/csj/sample.html の 学会講演  

## 解析結果
[result02.txt](results02.txt)  

## 所感
* 注）ダイアライゼーションはモノラルのみ対応  
* 分析結果は悪くない  
  * GCPと比較して、一長一短（GCPよりAzureの方が正確な箇所もあれば反対の場合もある）  
  * Azureだと句読点が振られるので便利。GCPに句読点を付ける方法はないのかな。。  
* 1人で話しているのになぜか2人いると認識された。。  
  * ダイアライゼーションをオンにすると、前提として2人いるという認識で分析される？  
  ->sample03のとおり、2人いる前提で分析しているような感じなので正確な話者識別ができなかったのでは  

# sample03（話者識別あり）
## 音源特徴
* 声色を変えて二人で話している体で録音  
* コールセンターのやり取りを想定  
* 原文  
```
1 すみません、化粧品について問い合わせたいんですけど。
2 はい、どの商品でしょうか。
1 そちらで購入した化粧水なんですが、液漏れしているみたいです。
2 申し訳ございません。交換させていただきます。
2 住所はどちらですか？
1 千代田区1丁目です。
2 承知しました。明日までに配送いたします。
1 ありがとうございます。
```

## 解析結果
[result03.txt](result03.txt)  

## 所感
* 概ね正確に記録できているが、端々で変な変換がされているところもある  
「はい、どの商品でしょうか」->「ファイトの商品でしょうか」  
「液漏れ」->「息漏れ」  
* 話者識別は完璧にできている  
とはいえ今回はわかりやすく話したので識別しやすかったと思われる  
実際の音声だとどうなるか  
* ちなみに感情分析をオンにしたら以下のエラーが…  
```
HTTP response body: {"code":"InvalidPayload","message":"This locale does not support sentiment analysis."}
```
残念ながら日本語は対応していないらしい  
