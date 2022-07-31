from xml.dom.minidom import Document
from sklearn.preprocessing import MinMaxScaler
from selenium.common.exceptions import NoSuchElementException
from flask import Flask, render_template, request, session, redirect, url_for
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time
import pandas as pd
import tweepy
import os
import wget
import numpy as np



app = Flask(__name__)
insta = []
faceb = []
tweet = []
images = []
array_fashion = ['#palazzopants', '#capri', '#oneshouldertop', '#trouser', '#tanktop', '#tubetop', '#satindress','#bodycondress', '#halterneck', '#poloneck', '#bikershort', '#camisole', '#sweatshirt', '#highwaistjeans', '#sharara', '#bellbottom', '#bomberjacket', '#leggings', '#vintageshirt', '#kimonocardigan', '#boilersuit', '#puffsleeves', '#coldshoulder', '#croptop', '#joggers', '#buckethat', '#poloshirt', '#sweatpants', '#rippedjeans', '#kaftandress', '#gown', '#cargopants', '#denimjacket', '#miniskirt', '#bratop', '#ponchos', '#polkadotdress', '#meshtop', '#hoodie', '#pullover', '#stripedshirt', '#jeggings', '#trenchcoat', '#waistcoat', '#blazer', '#offshoulder', '#denimshorts', '#loungewear', '#chinos', '#pencilskirt', '#floraldress', '#dhotipants', '#skaterdress', '#harempants', '#tees', '#dungaree', '#corset', '#peplumtop', '#jumpsuit', '#anarkalidress', '#lehenga', '#maxidress', '#yogapants', '#sherwani', '#sequencedress']

#Image links for the items rest data will be brought through social media. For user input images will will also be fetched
array_fashion_images = {
    "palazzopants" : ["https://rukminim1.flixcart.com/image/495/594/ked56kw0-0/trouser/u/c/3/free-tdzsp103-black-trendzmy-original-imafv28fq3htgsdd.jpeg?q=50", "https://rukminim1.flixcart.com/image/495/594/kg2l47k0-0/trouser/x/b/5/30-gladly35-34b-gladly-original-imafweafqzksfezk.jpeg?q=50", "https://rukminim1.flixcart.com/image/495/594/kybvo280/trouser/l/u/y/xxl-khadi-palazzo-wakshi-original-imagaha2teuewarq.jpeg?q=50", "https://rukminim1.flixcart.com/image/495/594/k13w4280/trouser/c/f/a/free-chickenplazzoo-kronmenien-original-imafhut7ycermapa.jpeg?q=50", "https://rukminim1.flixcart.com/image/495/594/l0vbukw0/trouser/6/y/o/xl-ac-new-02-areeba-collection-original-imagckc4zzbat5e5.jpeg?q=50"],
    "capri" : ["https://rukminim1.flixcart.com/image/800/960/khwbde80-0/capri/a/j/a/m-stwc-capri-black-pinkaop-sharktribe-original-imafxt68hzugknsa.jpeg?q=50", "https://rukminim1.flixcart.com/image/800/960/k547l3k0/capri/9/y/f/m-af-8010-styleaone-original-imafnuqsfwsfhv3c.jpeg?q=50", "https://rukminim1.flixcart.com/image/800/960/k572gsw0/capri/e/k/8/l-ccombo-02-8013-styleaone-original-imafnxeb2xgtdzmv.jpeg?q=50", "https://rukminim1.flixcart.com/image/800/960/kyrlifk0/capri/d/t/t/-original-imagax6nrzqyjyyg.jpeg?q=50", "https://rukminim1.flixcart.com/image/800/960/krqoknk0/capri/l/v/c/xl-mod-4106-combo31-modeve-original-imag5g3j6ccfkuxz.jpeg?q=50"],
    "oneshouldertop" : ["https://rukminim1.flixcart.com/image/495/594/ken59jk0/top/n/y/z/s-lady-76-lime-original-imafv9k5rzgjxfz4.jpeg?q=50", "https://rukminim1.flixcart.com/image/495/594/korijrk0/top/a/h/s/xs-sftops40035-sassafras-original-imag35curczchke9.jpeg?q=50", "https://rukminim1.flixcart.com/image/495/594/krf91u80/t-shirt/f/8/j/l-ttts000515-tokyo-talkies-original-imag57rm7mqwnfrc.jpeg?q=50", "https://rukminim1.flixcart.com/image/495/594/top/y/k/s/m-gr3732-black-harpa-original-imaer6gpppxhhkrd.jpeg?q=50", "https://rukminim1.flixcart.com/image/495/594/krf91u80/t-shirt/o/2/a/xl-ttts000517-tokyo-talkies-original-imag57rmnrbrphyn.jpeg?q=50"],
    "trouser" : ["https://rukminim1.flixcart.com/image/495/594/kb2jmvk0/trouser/g/u/k/44-t353-trouser-baleno-sgrey-aa36-ad-av-original-imafsgerqwzmehgs.jpeg?q=50", "https://rukminim1.flixcart.com/image/495/594/kzn17680/trouser/l/6/d/-original-imagbhuhegqtrgws.jpeg?q=50", "https://rukminim1.flixcart.com/image/495/594/kkyc9zk0/trouser/r/j/f/28-kctr-frml-99-crm-fubar-original-imagy6g4tp3vcr4k.jpeg?q=50", "https://rukminim1.flixcart.com/image/495/594/klv7ekw0/trouser/x/o/3/32-t685-trouser-baleno-babypink-aa-ad-av-original-imagyvqhhggsyfsy.jpeg?q=50", "https://rukminim1.flixcart.com/image/495/594/kdqa4y80-0/trouser/6/k/i/s-70sj070trwht-sajke-original-imafukptsqdwhkmr.jpeg?q=50"],
    "tanktop" : ["https://rukminim1.flixcart.com/image/495/594/kyhlfgw0/top/9/j/f/-original-imagapzwstwwctz8.jpeg?q=50", "https://rukminim1.flixcart.com/image/495/594/l2z26q80/top/2/w/h/xs-173-white-aahwan-original-image73jhdy73x5h.jpeg?q=50", "https://rukminim1.flixcart.com/image/495/594/kms2j680/top/s/p/s/m-at-5002-style-club-original-imagfht6zczwshbb.jpeg?q=50", "https://rukminim1.flixcart.com/image/495/594/l4u7vrk0/top/u/2/g/m-173-green-aahwan-original-imagfn5ybvhd9bhx.jpeg?q=50", "https://rukminim1.flixcart.com/image/495/594/juwzf680/top/z/x/k/m-7231696-hrx-by-hrithik-roshan-original-imaffvxdabvqgv38.jpeg?q=50"],
    "tubetop" : ["https://rukminim1.flixcart.com/image/495/594/l0fm07k0/top/k/u/d/xs-179-black-aahwan-original-imagc83kqvakemqx.jpeg?q=50", "https://rukminim1.flixcart.com/image/495/594/kctf0cw0/top/j/w/e/xs-59790701-puma-original-imaftujaaj7rkjfr.jpeg?q=50", "https://rukminim1.flixcart.com/image/495/594/l0bbonk0/top/9/y/8/l-cdbt-2000-nuevosdamas-original-imagc4zgnrfavr9m.jpeg?q=50", "https://rukminim1.flixcart.com/image/495/594/kyrlifk0/top/v/p/t/l-cl-wm-t0029-addyvero-original-imagaxdaydnynhg6.jpeg?q=50", "https://rukminim1.flixcart.com/image/495/594/kyrlifk0/top/3/w/l/l-cl-wm-t0030-addyvero-original-imagaxdayxhdzhus.jpeg?q=50"],
    "satindress" : ["https://rukminim1.flixcart.com/image/495/594/l4zxn680/dress/9/c/3/s-1205nd-nuevosdamas-original-imagfrmhx6hkasfr.jpeg?q=50", "https://rukminim1.flixcart.com/image/495/594/kyrlifk0/dress/p/d/s/l-1205-fkube-original-imagaxe3pbftunsg.jpeg?q=50" ,"https://rukminim1.flixcart.com/image/495/594/kziqvm80/dress/i/c/h/s-3756-the-dry-state-original-imagbghxcpktrxst.jpeg?q=50", "https://rukminim1.flixcart.com/image/495/594/kr3tj0w0/dress/p/7/z/m-1205-fkube-original-imag4z9geevgrqxs.jpeg?q=50", "https://rukminim1.flixcart.com/image/495/594/kvvad8w0/dress/r/4/b/m-d19604-18-u-f-original-imag8zek26hg8nzj.jpeg?q=50"],
    "bodycondress" : ["https://rukminim1.flixcart.com/image/495/594/kzblocw0/dress/u/y/o/l-1451-sheetal-associates-original-imagbd3cgxuvkwfu.jpeg?q=50", "https://rukminim1.flixcart.com/image/495/594/ku2zjww0/dress/c/l/1/s-1143-sheetal-associates-original-imag7aa2fyu9cakg.jpeg?q=50", "https://rukminim1.flixcart.com/image/495/594/l15bxjk0/dress/g/7/4/m-1453-sheetal-associates-original-imagcrxzsqzxecgc.jpeg?q=50", "https://rukminim1.flixcart.com/image/495/594/l4bn5ow0/dress/i/x/t/s-1611-sheetal-associates-original-imagf95zt93nwy9r.jpeg?q=50", "https://rukminim1.flixcart.com/image/495/594/kq6yefk0/dress/v/2/8/m-1083-sheetal-associates-original-imag49m2ggkzgekv.jpeg?q=50"],
    "halterneck" :["https://rukminim1.flixcart.com/image/495/594/l3j2cnk0/top/m/u/f/xs-184-black-aahwan-original-imagemrqhscegbzj.jpeg?q=50", "https://rukminim1.flixcart.com/image/495/594/l0jwbrk0/top/5/r/i/s-tttp005912-tokyo-talkies-original-imagcb3vg8zzmd86.jpeg?q=50", "https://rukminim1.flixcart.com/image/495/594/l3j2cnk0/top/g/3/f/s-184-white-aahwan-original-imagemrqytphpsna.jpeg?q=50", "https://rukminim1.flixcart.com/image/495/594/l071d3k0/top/v/i/r/xl-tttp005723-tokyo-talkies-original-imagcfgzfr94zdv8.jpeg?q=50", "https://rukminim1.flixcart.com/image/495/594/kmgn0cw0/top/j/f/c/free-belly-top-1-pink-the-dance-bible-original-imagfcd8qdggxfet.jpeg?q=50"],
    "poloneck" :["https://rukminim1.flixcart.com/image/495/594/khnqqa80-0/t-shirt/1/f/n/xl-t285hs-as7whdngr-seven-rocks-original-imafxma4svhfgfqp.jpeg?q=50", "https://rukminim1.flixcart.com/image/495/594/l1grgcw0/t-shirt/x/o/5/m-t428hs-tm5p-eyebogler-original-imagdf2egzjxeqgk.jpeg?q=50", "https://rukminim1.flixcart.com/image/495/594/l52sivk0/t-shirt/g/f/q/m-bppmp2806-black-pigeon-original-imagfu68zdyyvhh6.jpeg?q=50", "https://rukminim1.flixcart.com/image/495/594/kzegk280/t-shirt/8/9/b/s-t285hs-as7whblon-eyebogler-original-imagbfyfnkkbfjbg.jpeg?q=50", "https://rukminim1.flixcart.com/image/317/380/kzegk280/t-shirt/j/5/j/xs-t51-eyebogler-original-imagbf497cun2hwx.jpeg?q=50"],
    "bikershort" : ["https://rukminim1.flixcart.com/image/495/594/ktizdzk0/short/2/z/z/l-white-shorts-l-good-connection-original-imag6uxwuckdhwhd.jpeg?q=50", "https://rukminim1.flixcart.com/image/495/594/kn7sdjk0/short/q/5/r/m-sb-tri-combo-294-sober-black-original-imagfy69v8e52nuk.jpeg?q=50", "https://rukminim1.flixcart.com/image/495/594/l432ikw0/short/r/i/y/l-sb-shorts-294-sober-black-original-imagf2adwzdg8g9x.jpeg?q=50", "https://rukminim1.flixcart.com/image/495/594/kuyf8nk0/short/t/p/9/xxl-black-shorts-set2-xxl-good-connection-original-imag7yc8d8zz3cfw.jpeg?q=50", "https://rukminim1.flixcart.com/image/495/594/kzn17680/short/f/a/3/m-en48tl-pkt-shrt-everdion-original-imagbhumeztz6syt.jpeg?q=50"],
    "camisole" : ["https://rukminim1.flixcart.com/image/495/594/kw9krrk0/camisole-slip/8/l/b/xl-camyy-wsb-3-amosio-original-imag8z8v3cuzdwtc.jpeg?q=50", "https://rukminim1.flixcart.com/image/495/594/l48s9zk0/camisole-slip/h/1/q/m-1-fw-15-black-q-rious-original-imagf6yzxfpfcs6f.jpeg?q=50", "https://rukminim1.flixcart.com/image/495/594/ksoz53k0/camisole-slip/o/q/e/xs-ideal-for-teens-and-womens-digsel-cottons-original-imag677ehs8buecz.jpeg?q=50", "https://rukminim1.flixcart.com/image/495/594/camisole-slip/f/p/k/halt-u-5-q-rious-m-original-imae8mrd7cczdfzg.jpeg?q=50", "https://rukminim1.flixcart.com/image/495/594/k5zn9u80/camisole-slip/8/4/6/xxl-cami-mgrey-leading-lady-original-imafacqcpexctqmg.jpeg?q=50"],
    "sweatshirt" : ["https://rukminim1.flixcart.com/image/495/594/kfpq5jk0/sweatshirt/u/c/t/4xl-togrblhdfulsweat-believer-tripr-original-imafw3cfjfjxtjgv.jpeg?q=50", "https://rukminim1.flixcart.com/image/495/594/kdyus280/sweatshirt/w/6/e/l-szf-3pnl-sweat-skittzz-original-imafuqx6knyjg5ey.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/ked56kw0/sweatshirt/y/h/w/4xl-tblhdfullsweat-lion-tripr-original-imafvfthvnwhhpzs.jpeg?q=50", "https://rukminim1.flixcart.com/image/495/594/k1gr2q80/sweatshirt/r/g/u/m-929217fk-breil-by-fort-collins-original-imafkx3tz4q7jw2w.jpeg?q=50", "https://rukminim1.flixcart.com/image/495/594/krf91u80/sweatshirt/t/i/g/xl-1jgswdd2-red-jugular-original-imag57wy8hnz2fxp.jpeg?q=50"],
    "highwaistjeans" : ["https://rukminim1.flixcart.com/image/495/594/kdnf98w0-0/jean/6/p/g/36-7b-highwaiste-blk-broadstar-original-imafuggw9akskzcj.jpeg?q=50", "https://rukminim1.flixcart.com/image/495/594/kdbzqfk0/jean/8/3/b/32-559884-blue-poison-original-imafu9b98ntcnkgn.jpeg?q=50", "https://rukminim1.flixcart.com/image/495/594/l34ry4w0/jean/n/k/x/30-cr-wj-1088-ibl-crazeis-original-imagebp8qjzq6jfz.jpeg?q=50", "https://rukminim1.flixcart.com/image/495/594/kvtuxe80/jean/z/n/h/30-wjr-02-4b-kc-fur-editlook-original-imag8n4d4g6vst5w.jpeg?q=50", "https://rukminim1.flixcart.com/image/495/594/k7ry3680/jean/8/q/h/28-ladiesjeans-11-german-club-original-imafpy66gbztvx7y.jpeg?q=50"],
    "sharara" : ["https://rukminim1.flixcart.com/image/495/594/kyuge4w0/trouser/y/j/v/xl-shararapalazzo-01-vaanya-original-imagazm49bpxzker.jpeg?q=50", "https://rukminim1.flixcart.com/image/495/594/ktyp8cw0/trouser/q/x/0/free-pi-whitesharara-001-pi-world-original-imag7729h5khgg46.jpeg?q=50", "https://rukminim1.flixcart.com/image/495/594/kmi2g7k0/trouser/4/q/k/free-ew-sh-pink-mirror-14-emmy-word-original-imagfeah4y7evdsa.jpeg?q=50", "https://rukminim1.flixcart.com/image/317/380/kku1yfk0/pyjama/q/z/v/xl-ss21gs173shrchd-global-desi-original-imagy3gj3kjjgatj.jpeg?q=50", "https://rukminim1.flixcart.com/image/495/594/l0o6nbk0/trouser/9/i/t/free-fm-04-viara-original-imagcew9kgaw5vyx.jpeg?q=50"],
    "bellbottom" : ["https://rukminim1.flixcart.com/image/495/594/l0igvww0/jean/o/r/p/32-mt07-bb-bell-bottom-metronaut-original-imagcab5dthvhsgg.jpeg?q=50", "https://rukminim1.flixcart.com/image/495/594/l0igvww0/jean/u/j/k/30-mt07-bb-bell-bottom-metronaut-original-imagcab5byjzz8hp.jpeg?q=50", "https://rukminim1.flixcart.com/image/495/594/l4u7vrk0/jean/8/9/h/28-bell-bottom-blue-28-seematex-original-imagfnf7qkkcjfyh.jpeg?q=50", "https://rukminim1.flixcart.com/image/495/594/koq33ww0/trouser/h/a/q/free-lplblue-free-eyelook-original-imag3483ctknmhuj.jpeg?q=50", "https://rukminim1.flixcart.com/image/495/594/l51d30w0/trouser/s/w/x/xl-313-bell-bottom-al-hudooms-original-imagft25zzxcmeyc.jpeg?q=50"],
    "bomberjacket" : ["https://rukminim1.flixcart.com/image/495/594/kflftzk0/jacket/h/m/r/l-blaw20jkt02a-billion-original-imafwyyrcjn3cecz.jpeg?q=50", "https://rukminim1.flixcart.com/image/495/594/k3orqfk0/jacket/n/x/t/xxl-10679220-roadster-original-imafmqera6pbhc94.jpeg?q=50", "https://rukminim1.flixcart.com/image/495/594/km57hjk0/jacket/a/m/p/l-mod-1014-wine-modeve-original-imagf43adg5q3edh.jpeg?q=50", "https://rukminim1.flixcart.com/image/495/594/kf75fgw0/jacket/f/z/m/m-mod-1004-camel-modeve-original-imafvpbp82ykjmfd.jpeg?q=50", "https://rukminim1.flixcart.com/image/495/594/kh2b4i80/jacket/q/6/v/m-pcjkcbof749924-peter-england-original-imafx4szhkpn3quw.jpeg?q=50"],
    "leggings" : ["https://rukminim1.flixcart.com/image/495/594/kf8kvbk0/legging/v/r/d/free-lns-brs-k-m-r-garments-original-imafvq7fg67cpw2a.jpeg?q=50", "https://rukminim1.flixcart.com/image/495/594/kfikya80/legging/s/s/a/xl-ikl-4-wbpr-xl-ikhlas-original-imafvy43h3rzzzyw.jpeg?q=50", "https://rukminim1.flixcart.com/image/495/594/jsw3yq80/kids-legging/z/f/x/6-7-years-aoleg-10-model-6-fantastic-fit-original-imafecmv3mbznew6.jpeg?q=50", "https://rukminim1.flixcart.com/image/495/594/l4iscy80/legging/y/g/6/free-ankle-length-vivaan-retail-original-imagfehfumgt5tqz.jpeg?q=50", "https://rukminim1.flixcart.com/image/495/594/klzhq4w0/legging/7/w/i/xxl-2legg-k-m-r-garments-original-imagyzzkuxqdc8j7.jpeg?q=50"],
    "vintageshirt" : ["https://rukminim1.flixcart.com/image/495/594/k5o7r0w0/shirt/b/a/e/l-udsh0525-u-s-polo-assn-original-imafz9mxyef5tqsv.jpeg?q=50", "https://rukminim1.flixcart.com/image/495/594/k3g73bk0/shirt/r/z/k/l-pm306261ua0-pepe-jeans-original-imafmkrbvu7ugcre.jpeg?q=50", "https://rukminim1.flixcart.com/image/495/594/k12go7k0/shirt/m/q/g/40-lrsfcslpo05131-louis-philippe-jeans-original-imafkqasurmrkufk.jpeg?q=50", "https://rukminim1.flixcart.com/image/495/594/jmp79u80/shirt/g/v/9/m-136326-scotch-soda-original-imaf9jcsgawegqga.jpeg?q=50", "https://rukminim1.flixcart.com/image/495/594/kc9eufk0/shirt/k/2/r/l-pm306610-olive-pepe-jeans-original-imaftf9kjgahrhrm.jpeg?q=50"],
    "kimonocardigan" : ["https://rukminim1.flixcart.com/image/495/594/jxp08sw0/shrug/b/k/z/xl-ss-009-shrug-009-handicraft-palace-original-imafg2gbmyhytj22.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/ju8oxow0/shrug/b/h/h/xl-tds0002-shrug02-handicraft-palace-original-imaffezfdcwfzhuj.jpeg?q=50", "https://rukminim1.flixcart.com/image/495/594/jxp08sw0/shrug/s/9/f/xl-ss-0011-shrug-0011-handicraft-palace-original-imafg2gjrc7px8kf.jpeg?q=50", "https://rukminim1.flixcart.com/image/495/594/ju8oxow0/shrug/v/7/r/xl-tds0006-shrug06-handicraft-palace-original-imaffezsfzy3zfxd.jpeg?q=50", "https://rukminim1.flixcart.com/image/495/594/jxnksy80/shrug/d/n/p/xl-ss-008-shrug-008-handicraft-palace-original-imafg2g4dy2t2hg4.jpeg?q=50"],
    "boilersuit" : ["https://rukminim1.flixcart.com/image/612/612/kn0n6a80/paint-coverall/a/t/r/xl-coverall-blue-boiler-suit-for-men-solitaire-original-imagfsbyzn7zsutj.jpeg?q=70","https://rukminim1.flixcart.com/image/612/612/kw6pw280/paint-coverall/a/h/m/m-grey-plain-boiler-suit-size-m-made-up-of-100-soft-cotton-of-original-imag8x59emzggckd.jpeg?q=70","https://rukminim1.flixcart.com/image/612/612/kjlrb0w0-0/paint-coverall/o/o/s/xl-men-s-cotton-safety-coverall-boiler-suit-rssw-original-imafz59hbqczr3zg.jpeg?q=70","https://rukminim1.flixcart.com/image/612/612/kq2o2vk0/paint-coverall/v/y/f/s-boiler-suit-orange-full-sleeve-s-of-240-gsm-associated-original-imag463gzh68uufb.jpeg?q=70","https://rukminim1.flixcart.com/image/612/612/kn4xhu80/paint-coverall/n/n/c/xl-workwear-men-s-cotton-coverall-boiler-suit-ca-1003-m-club-original-imagfvy5wghfhez3.jpeg?q=70"],
    "puffsleeves" : ["https://rukminim1.flixcart.com/image/495/594/ksaoqkw0/top/w/l/x/l-tris-top-03-trislin-original-imag5w5cbdhntgga.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/kflftzk0/top/h/x/z/s-2447-buynewtrend-original-imafwyzkdjtzhucg.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/koad9jk0/top/r/w/z/s-0078-top-dl-fashion-original-imag2rzffnkbgrzz.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/kxrvi4w0/dress/j/q/f/xxl-bottleblue-tierdres1-isam-original-imaga5q7yfn9nrmp.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/kqv8vww0/top/z/d/b/m-ulss19tp09-37-013-uptownie-lite-original-imag4scyutrzrhzh.jpeg?q=50"],
    "coldshoulder" : ["https://rukminim1.flixcart.com/image/495/594/kbi9h8w0/top/b/x/h/m-tttp003710-tokyo-talkies-original-imafsugxpegyw9ff.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/l41n2q80/top/c/l/u/s-mwss22tsrt043a-metronaut-original-imagff2gukz8ntwk.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/l44hyfk0/top/8/s/e/s-ksltops1755-kassually-original-imagf3azzjrjhtue.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/jrs3mvk0/top/n/j/t/s-ep2140c-rare-original-imafdhh4zd5jay4t.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/kz4gh3k0/top/d/u/3/-original-imagb789pzx8nucm.jpeg?q=50"],
    "croptop" : ["https://rukminim1.flixcart.com/image/495/594/l186t8w0/top/w/d/n/xl-rc-black-top-skirt-teekhi-girl-original-imagcuavug9qzjec.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/kfwvcsw0/top/j/f/s/3xl-jb-117-blkylwwht-juneberry-original-imafw9h2mrgj4qry.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/kgjqefk0/top/f/h/5/s-bj-top0324-febia-original-imafwrhyxkyjavyv.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/l572ufk0/top/3/g/x/s-188-white-aahwan-original-imagfx8cpnvthxww.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/kqb8pzk0/top/t/9/6/l-00142-ct-dl-fashion-original-imag4cfggagzym55.jpeg?q=50"],
    "joggers" : ["https://rukminim1.flixcart.com/image/495/594/l3rmzrk0/jean/m/l/8/28-6703-dbl-metronaut-original-imagetk9zfy4cpfg.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/kr3tj0w0/jean/n/j/k/34-ud0045-united-denim-original-imag4z2fxambuawm.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/knj7wcw0/jean/d/t/p/34-z1-jog-05-zaysh-original-imag26wdnew72ubf.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/jhavdzk0/jean/j/x/p/30-hpsjogger-lgrey-urbano-fashion-original-imaf5bzbhhvwu9by.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/kp78e4w0/jean/z/m/u/32-jk-jog02-zaysh-original-imag3h9hc9gknzd6.jpeg?q=50"],
    "buckethat" : ["https://rukminim1.flixcart.com/image/612/612/kzzw5u80/hat/g/7/m/latest-reversible-hat-free-1-trendy-cow-reversible-hat-h-original-imagbvbyugvubfyp.jpeg?q=70","https://rukminim1.flixcart.com/image/612/612/kylvr0w0/hat/s/c/f/latest-stylish-butterfly-design-reversible-hat-free-1-hat-2-original-imagash4zhbpng3t.jpeg?q=70","https://rukminim1.flixcart.com/image/612/612/l2p23rk0/hat/b/i/8/dbgr-1-free-1-dbgr-1-dbgr1-ambitieux-original-imagdzcm2ehjyndh.jpeg?q=70","https://rukminim1.flixcart.com/image/612/612/kyoqmq80/hat/h/c/z/h-4-free-1-latest-cute-big-smiley-hat-hat-4-highever-original-imagauhavgnpuc3x.jpeg?q=70","https://rukminim1.flixcart.com/image/612/612/l13whow0/shower-cap/f/e/u/children-s-bucket-hat-with-fish-design-outdoor-sun-hat-4-12-original-imagcrynf35aterj.jpeg?q=70"],
    "poloshirt" : ["https://rukminim1.flixcart.com/image/495/594/kzegk280/shirt/t/e/c/m-udshto0183-u-s-polo-assn-original-imagbfyhtdgc99rw.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/kxxl9jk0/shirt/f/x/v/3xl-usshtd0170-u-s-polo-assn-original-imagaa65ahh8fpmp.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/kw9krrk0/shirt/2/2/r/s-ustsh0693-u-s-polo-assn-original-imag8zgzxqkp4yya.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/kzegk280/shirt/5/q/3/m-usshto0875-u-s-polo-assn-original-imagbf5ayggczhhr.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/l111lzk0/shirt/h/j/f/xxl-udsht0362-u-s-polo-assn-original-imagczjp3wzfsczy.jpeg?q=50"],
    "sweatpants" : ["https://rukminim1.flixcart.com/image/495/594/l1jmc280/track-pant/h/w/p/s-solid-men-black-blue-track-pants-foxter-original-imagd36hzpbqrasp.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/jxtakcw0/track-pant/z/2/d/xs-1847682-hrx-by-hrithik-roshan-original-imafg6xvjtckzgj3.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/kua4r680/track-pant/z/x/q/l-patti1-acrux-original-imag7fwxgrxrdt6z.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/kixgtjk0-0/kids-track-pant/z/q/k/7-8-years-tblgy-wmboyjogger-crosline-tripr-original-imafym78az6vm8um.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/kixgtjk0-0/kids-track-pant/z/q/k/7-8-years-tblgy-wmboyjogger-crosline-tripr-original-imafym78az6vm8um.jpeg?q=50"],
    "rippedjeans" : ["https://rukminim1.flixcart.com/image/495/594/k0463rk0/jean/n/g/b/32-8903579-roadster-original-imafjuyhtjgwn4j4.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/kzpw2vk0/jean/9/d/b/28-f0004-tracknjeans-original-imagbz9afwdbwbzk.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/kr6oeq80/jean/d/y/u/38-hljn001422-highlander-original-imag5fy9b4xjsnrn.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/krayqa80/jean/k/i/0/32-mss21jn683-metronaut-original-imag54h5hfh7yzhr.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/l3rmzrk0/jean/u/v/e/32-lmjn007746-locomotive-original-imagethbgsxqfyta.jpeg?q=50"],
    "kaftandress" : ["https://rukminim1.flixcart.com/image/495/594/kyeqjrk0/dress/6/v/z/xxl-smf55-beigekaftan-smita-fashion-original-imaganfhzqj35fd7.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/ktketu80/dress/6/o/r/free-kaftan-multi8-suvasana-original-imag6vkx9h6zhmem.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/kupuljk0/dress/r/3/r/s-k-94-kaftan-dress-shyam-sundari-original-imag7rwhzhsqpvee.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/l1qrjbk0/dress/m/d/w/xl-201-d-kaftan-pink-jsr-shopaxis-original-imagd8vgwfzhwxtu.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/ktszgy80/kaftan/k/s/x/free-af260-fvogue-original-imag7fu49xhmhwqe.jpeg?q=50"],
    "gown" : ["https://rukminim1.flixcart.com/image/495/594/k0lbdzk0/gown/j/h/4/na-l-gown151-hiva-trendz-na-month-original-imafj5ddepwrqhyf.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/k0lbdzk0/gown/v/f/a/na-l-gown152-hiva-trendz-na-original-imafj5dfb59rvyyx.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/xif0q/gown/q/c/d/na-xxl-short-sleeve-stitched-ss-04-jash-creation-na-original-imag3hyesubkhaxw-bb.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/l0cr4i80/gown/p/l/x/na-xl-3-4-sleeve-stitched-ss-40-femvy-na-original-imagc5mtfpzsz6tp.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/l0cr4i80/gown/w/h/p/na-s-3-4-sleeve-stitched-ss-40-femvy-na-original-imagc5mtdajhchqu.jpeg?q=50"],
    "cargopants" : ["https://rukminim1.flixcart.com/image/495/594/kziqvm80/track-pant/p/a/m/xl-fc2053-track-fastcolors-original-imagbggg6gsgtpgh.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/knhsgi80/cargo/v/3/u/26-cargo-black-26-tohubohu-original-imag25m3wpebafpb.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/kzogn0w0/cargo/x/o/i/xxl-fc2056-fastcolors-original-imagbmr4xm2jsfwe.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/k4k7f680/cargo/s/j/g/32-sf-32-grey-cargo-stylefit-original-imafhhtzghcgmvjj.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/l3es13k0/cargo/c/d/i/3-4-years-skg-army-202-boys-cargo-pant-skgkidswear-original-imagejzqfacjspee.jpeg?q=50"],
    "denimjacket" : ["https://rukminim1.flixcart.com/image/495/594/jxw5g280/jacket/6/2/g/xl-mntnw-4024-montrez-original-imafg82gbevyfwwz.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/km2clu80/jacket/c/f/0/s-mnt-7003-montrez-original-imagffv4hs3k6quc.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/km2clu80/jacket/l/v/6/xl-mnt-7004-montrez-original-imagffv4bk5bkfpy.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/ki3gknk0hlty2aw-0/jacket/0/z/i/l-1-jakt-denim-mblue-urbano-fashion-original-imafy3jhxpwggqeh.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/ks6ef0w0/jacket/x/h/p/xl-nmnt-7004-montrez-original-imag5t3nfpbqhgrx.jpeg?q=50"],
    "miniskirt" : ["https://rukminim1.flixcart.com/image/495/594/kv8fbm80/skirt/g/f/l/s-166-maroon-aahwan-original-imag86b5zmgzdyuh.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/kv8fbm80/skirt/g/q/z/m-166-black-aahwan-original-imag86b5gxrzgabh.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/kydb3ww0/skirt/b/c/t/28-ttst000780-tokyo-talkies-original-imagamaqckupuyzw.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/kv450280/skirt/k/f/r/28-ttst000700-tokyo-talkies-original-imag82tj8krqytyw.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/l1grgcw0/skirt/v/p/8/xl-5388-darzi-original-imagdymseggfbfhz.jpeg?q=50"],
    "bratop" : ["https://rukminim1.flixcart.com/image/495/594/kqqykcw0/bra/1/z/j/lightly-padded-34-regular-no-regular-queen010-lbw-30-x2-nizvira-original-imag4zz2dv9z7bey.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/ksnjp8w0/bra/m/k/k/lightly-padded-32-regular-no-styled-back-bralette-for-women-original-imag66dz2m5bmuyr.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/kq9ta4w0/bra/p/a/q/lightly-padded-28a-no-regular-regular-bralette-cikla-original-imag4bgp3fecztzs.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/l5bd5zk0/bra/f/n/c/lightly-padded-32-1-regular-no-low-back-comfortable-and-stylish-original-imaggypfufrfxbyd.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/ktop5e80/bra/p/g/s/lightly-padded-36-no-regular-regular-queen012-lbw-mrs-queen-original-imag6z7j2kydzapr.jpeg?q=50"],
    "ponchos" : ["https://rukminim1.flixcart.com/image/495/594/kwtkxow0/poncho/4/h/u/free-mod-3514-mustard-modeve-original-imag9f2jcp9n9trg.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/ku8pbbk0/poncho/3/r/t/free-mod-3503-red-modeve-original-imag7dzdanhffwef.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/jpr86fk0/poncho/s/h/c/free-beige2-icable-original-imafbxcet7ksgana.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/kw104nk0/poncho/w/h/8/free-mod-3511-beige-modeve-original-imag8sfj7zyn5jzn.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/kxp0mfk0/poncho/9/n/j/free-black-dot-poncho-discoveryline-original-imaga3hyh6x7xw39.jpeg?q=50"],
    "polkadotdress" : ["https://rukminim1.flixcart.com/image/495/594/kbdz5ow0/dress/j/x/p/l-2930-darzi-original-imafsqy4ugug5haq.jpeg?q=50","https://rukminim1.flixcart.com/image/317/380/kxz0pe80/dress/v/0/m/xs-dr902-stalk-original-imagaazaxxng6qng.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/k7assy80/dress/7/u/c/xxl-sfdrss1838-sassafras-original-imafpkcfkyyt2gxd.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/k7m8brk0/dress/f/s/3/m-drs-00200-bk-my-swag-original-imafpszb64cgfrvh.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/ktep2fk0/dress/b/w/o/xxl-1162-fkube-original-imag6r9mzjwfh6wk.jpeg?q=50"],
    "meshtop" : ["https://rukminim1.flixcart.com/image/495/594/kzzw5u80/top/3/t/h/m-sftops40513-sassafras-original-imagbvxdagmzqgh2.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/jshtk7k0/top/h/q/d/l-sftops4524-sassafras-original-imafdzv84qg8hjrg.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/kj7gwi80-0/top/f/z/j/m-am-1008-green-ara-fashion-original-imafytvwphxtnnxh.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/k69ncsw0/top/n/v/b/m-96tk2397-selvia-original-imafzrqfydfgztdw.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/l1grgcw0/top/9/g/q/xl-rc-flower-top-teekhi-girl-original-imagdyzhhckrkjwz.jpeg?q=50"],
    "hoodie" : ["https://rukminim1.flixcart.com/image/495/594/k4324y80/sweatshirt/a/x/z/7-8-years-faz-ss-03-fazza-original-imafnfw94y3nzfe9.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/kwzap3k0/sweatshirt/y/3/n/l-fc6049-fastcolors-original-imag9j6a9mxhskne.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/k4k7f680/sweatshirt/z/m/t/7-8-years-faz-ss-01-fazza-original-imafnfxu8gnjznzw.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/kxw5tow0/sweatshirt/o/g/r/xxl-avlogohoddie-013h-finwin-original-imaga8besgu5wzxu.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/kfzq8i80/sweatshirt/b/6/v/xl-tnvsweatskulbeard1-tripr-original-imafwbq59rhm5zmu.jpeg?q=50"],
    "pullover" : ["https://rukminim1.flixcart.com/image/495/594/j9rdq4w0/sweatshirt/c/2/a/xl-hoogreymilange-hoonavyblue-fleximaa-original-imaexb5nthhszw2h.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/k5y7tzk0/pullover/f/q/p/4xl-spn6-mustard-xxxxl-icable-original-imafdyxe3ruabgmf.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/j9rdq4w0/sweatshirt/c/3/m/xxl-hoomaroon-hooroyalblue-fleximaa-original-imaexkppaw6fmgv8.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/j9rdq4w0/sweatshirt/c/3/m/xxl-hoomaroon-hooroyalblue-fleximaa-original-imaexb5n6ghghuxg.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/j9u8lu80/sweatshirt/y/g/b/xxl-hoocharcoalmilange-hoored-fleximaa-original-imaexb5n2mhdvukp.jpeg?q=50"],
    "stripedshirt" : ["https://rukminim1.flixcart.com/image/495/594/xif0q/shirt/b/4/x/xxl-men-slim-fit-lining-away-collar-casual-shirt-icome-original-imag4kj8drnaeq5y-bb.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/xif0q/shirt/c/w/c/xl-h2-finivo-fashion-original-imagyzfc9x9ws9fn-bb.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/xif0q/shirt/n/j/h/m-200-combraided-original-imagavxewfgzhbb6-bb.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/xif0q/shirt/7/g/q/m-sh-black-line-u-turn-original-imagfsgdhhrkfh95-bb.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/xif0q/shirt/h/b/2/s-rs19stpw08-p-rope-original-imafwyfyffrcpxd2-bb.jpeg?q=50"],
    "jeggings" : ["https://rukminim1.flixcart.com/image/495/594/kfeamq80/jegging/g/5/q/4xl-ga048-mm-21-original-imafvvbjhrxb5hr9.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/k48rwcw0/jegging/2/e/8/4xl-ga049-mm-21-original-imafm8hwkuryhpk8.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/k6gsk280/jegging/h/b/k/m-ga050-mm-21-original-imafm8hwxskkxmrg.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/jw6pifk0/jegging/k/v/q/xs-9056993-roadster-original-imafgwg6jngs5m5d.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/kzzw5u80/jegging/k/l/g/l-wcp-cocbw-l-angarkha-original-imagbv38cgxhjtun.jpeg?q=50"],
    "trenchcoat" : ["https://rukminim1.flixcart.com/image/495/594/k3g73bk0/coat/r/v/n/xl-ccj19112385-color-cocktail-original-imafmknuvsnhevcx.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/ja8j0cw0/coat/2/j/k/xl-ajk-1767-athena-original-imaezurzwpyfgrrm.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/ja8j0cw0/coat/4/c/a/xl-ajk-1766-athena-original-imaezurzzgakbf6x.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/ja8j0cw0/coat/k/y/h/xxl-ajk-1759-athena-original-imaezurzxxystq4s.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/ja8j0cw0/coat/f/t/g/xl-ajk-1762-athena-original-imaezurzeznzdraj.jpeg?q=50"],
    "waistcoat" : ["https://rukminim1.flixcart.com/image/495/594/waistcoat/u/z/e/qalblue-qalamkari-42-original-imaeprdpfcfvpxkf.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/kehfi4w0/waistcoat/f/n/m/40-wngr-05-trulyfab-original-imafv5fhfmmxxgv9.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/kq2o2vk0/waistcoat/8/5/z/4-5-years-211-black-aj-dezines-original-imag464pj6nmxfgz.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/kubk70w0/waistcoat/w/v/h/38-pinjotlfw69097-peter-england-original-imag7gz479gg4t2t.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/j0wqj680/waistcoat/2/h/c/46-qalmaroon-qalamkari-original-imaeq599bwwr3bbk.jpeg?q=50"],
    "blazer" : ["https://rukminim1.flixcart.com/image/495/594/l2rwzgw0/blazer/k/s/s/40-pmjl02731-g2-park-avenue-original-imagefzybvhhvkcs.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/kskotjk0/blazer/f/k/p/46-142082802-jack-jones-original-imag63v6zc8rktzc.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/kuyf8nk0/blazer/7/i/q/40-vsbzwslpp84228-van-heusen-sport-original-imag7yrym7qsndhd.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/kvr01ow0/blazer/h/q/u/l-blazer-alfa-hub-original-imag8h3azacz3bn2.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/l2ghgnk0/blazer/2/5/s/40-pmjl02731-b4-park-avenue-original-imagdsqpjjgfvc8h.jpeg?q=50"],
    "offshoulder" : ["https://rukminim1.flixcart.com/image/495/594/kzsqykw0/dress/e/n/g/m-1516-sheetal-associates-original-imagbqcjmwgtvzxy.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/ku8pbbk0/dress/b/x/s/xl-sn-dr-74-slenor-original-imag7emersm9wkgs.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/kr2e3680/top/h/1/e/m-off-shoulder-lime-n-lemon-original-imag4xvehecxyphc.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/l3dcl8w0/top/v/k/f/m-tttp006206-tokyo-talkies-original-imageg3b8ydfpvgy.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/kxnl6kw0/top/m/m/3/s-fh-consie-dori-teekhi-girl-original-imaga258kvzrwpd7.jpeg?q=50"],
    "denimshorts" : ["https://rukminim1.flixcart.com/image/495/594/km2clu80/short/a/x/l/32-r-1418-bata-32-mantock-original-imagff7jyf7bf56c.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/kcp4osw0/short/c/n/x/28-11489666-roadster-original-imaftrn2vhsdzduw.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/kcp4osw0/short/q/r/k/34-11489520-roadster-original-imaftrnfcxyxwech.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/km2clu80/short/c/r/k/26-m-1425-bata-26-mantock-original-imagff7qhzujbgdv.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/l4iscy80/short/i/f/e/32-mnt-3018-montrez-original-imagfe9x8kseahhy.jpeg?q=50"],
    "loungewear" : ["https://rukminim1.flixcart.com/image/495/594/kpr8k280/short/w/1/q/m-scombo-02-at-7001-style-club-original-imag3x9gc8w2ckg3.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/ks6ef0w0/short/n/o/3/s-rx10-0103-lavsc-jockey-original-imag5spruatwy3zw.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/kkzrpu80/short/h/9/5/m-wshot-blkcamo-hashbean-original-imagy7y7jnudchrj.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/l0igvww0/short/w/s/s/l-women-shorts-jocker-original-imagca9grjqyz528.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/ksru0sw0/short/u/9/k/s-rx15-0103-cnavy-jockey-original-imag69gb6fk5gva2.jpeg?q=50"],
    "chinos" : ["https://rukminim1.flixcart.com/image/495/594/k6ci8i80/trouser/q/w/t/34-10953540-roadster-original-imafzt9wdvmunhdz.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/kpedle80/trouser/y/v/c/32-13859528-roadster-original-imag3mzefczxnnre.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/l4yi7bk0/trouser/c/q/p/36-4509-blends-trendz-original-imagfqs7tzrycst8.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/l41n2q80/trouser/u/9/c/32-maw21ct304j-metronaut-original-imagff3q7fuhehn7.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/kfbfr0w0-0/trouser/j/v/c/32-astfwsrfd74972-allen-solly-original-imafvswruyfyqyny.jpeg?q=50"],
    "pencilskirt" : ["https://rukminim1.flixcart.com/image/495/594/kjkbv680-0/skirt/c/w/e/26-kttwomensskirt42-kotty-original-imafz3qg9cvswcz3.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/k1gr2q80/skirt/h/y/h/l-mid-thigh-length-pencil-skirt-neu-look-original-imafhfajbxmxvzsd.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/kl421e80/skirt/j/d/m/xl-3390-darzi-original-imagyaxeckuwatvm.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/l0lbrm80/skirt/j/j/i/28-kttwomensskirt77-kotty-original-imagccg4uf8z5z6y.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/ksdjma80/skirt/a/i/5/34-ttst000651-tokyo-talkies-original-imag5ygz8gzd89kc.jpeg?q=50"],
    "floraldress" : ["https://rukminim1.flixcart.com/image/495/594/kpinwy80/dress/1/o/b/l-2frock-185-186-hiva-trendz-original-imag3qdfb6hzwmsr.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/l071d3k0/dress/u/p/g/s-302tk8035-selvia-original-imagcf8enq5bydtp.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/l0h1g280/dress/1/4/8/l-pinktierdress1-isam-original-imagc98tpyztfy7x.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/l4x2rgw0/dress/n/b/k/m-sc20es49-suiwal-s-original-imagfpeu8ggj9zex.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/kt0enww0/dress/2/d/p/xxl-1091-sheetal-associates-original-imag6g4n7qhwesad.jpeg?q=50"],
    "dhotipants" : ["https://rukminim1.flixcart.com/image/495/594/l0igvww0/harem-pant/l/w/i/free-dti-pkt-pursa-original-imagcahwzg4hdzns.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/kjym9ow0/harem-pant/h/o/c/free-dhoti12-pink-nymex-original-imafzesvbuggbrnm.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/l0vbukw0/harem-pant/a/l/i/36-acpnp26099-sellingsea-original-imagcjzyg43zxrms.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/ki4w0i80-0/dhoti/a/n/c/free-dht-lalymart-original-imafxzrz9j3zqngx.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/klwmufk0/harem-pant/d/q/5/free-bttm1062-sarjuke-original-imagyxzbggzytzh6.jpeg?q=50"],
    "skaterdress" : ["https://rukminim1.flixcart.com/image/495/594/khavrm80-0/dress/f/l/n/xxl-dress-226-daevish-original-imafxchtedxbzszb.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/kw3v0cw0/dress/j/e/i/l-224-raaka-original-imag8v2ndhdyze3w.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/kflftzk0/dress/z/6/7/l-cl-wm-u0442-addyvero-original-imafwyxnxega8dab.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/kpinwy80/dress/n/y/i/m-2frock-183-184-hiva-trendz-original-imag3qdfkhgadwdr.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/kx7vc7k0/dress/g/m/r/-original-imag9q9wufrmhmum.jpeg?q=50"],
    "harempants" : ["https://rukminim1.flixcart.com/image/495/594/l3929ow0/harem-pant/y/p/b/free-whp-23-103-mgrandbear-original-imageezh2azu7c5q.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/kybvo280/harem-pant/2/p/j/xl-leaf-blue-and-maroon-yoosha-original-imagahahf7ejveyt.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/l3es13k0/harem-pant/9/v/t/free-whp-57-160-mgrandbear-original-imagejggznkre3gh.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/kn0n6a80/harem-pant/q/i/p/free-nn1922018hpcb-nnifa-original-imagfsj2g7xd7hy3.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/kqse07k0/harem-pant/i/q/y/free-whp-52-129-mgrandbear-original-imag4qfxxtgjcghh.jpeg?q=50"],
    "croptop" : ["https://rukminim1.flixcart.com/image/495/594/kfwvcsw0/top/j/f/s/3xl-jb-117-blkylwwht-juneberry-original-imafw9h2mrgj4qry.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/kruyw7k0/top/h/h/w/m-140-wudly-original-imag5k7hxcvhyubu.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/kwl0akw0/top/j/r/p/xs-tttp005279-tokyo-talkies-original-imag983aujmxzxaq.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/kz4gh3k0/top/a/q/k/l-tttp005971-tokyo-talkies-original-imagb7d9yswxgguz.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/xif0q/top/l/7/q/m-crop-love-white-adonyx-original-imagghg5hjnspdfh.jpeg?q=50"],
    "tees" : ["https://rukminim1.flixcart.com/image/495/594/xif0q/t-shirt/b/6/d/l-bylrn-z31-blive-original-imagbkqgknxgmncw-bb.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/l0vbukw0/t-shirt/i/t/6/m-tylrn-d51-tripr-original-imagck92uwy6wm45.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/ky1vl3k0/t-shirt/s/8/0/m-hs-hanuman-orange-young-trendz-original-imagadfyaf39mtfj.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/l0sgyvk0/t-shirt/a/w/a/l-bblwmrnful-z53-blive-original-imagcg65qwbgqm4a.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/l4hcx3k0/t-shirt/x/q/4/s-53681544-puma-original-imagfd75hh9vvpfk.jpeg?q=50"],
    "dungaree" : ["https://rukminim1.flixcart.com/image/495/594/k687wy80/dungaree-romper/v/p/k/s-2055b-buynewtrend-original-imafzqdbafazxmqg.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/kw9krrk0/dungaree-romper/d/1/r/s-33507-urbanic-original-imag8zcph4vshfev.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/ksru0sw0/short/a/v/j/xs-42498-urbanic-original-imag69t3yemggnzr.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/kgwld3k0/dungaree-romper/y/s/h/s-bhavya-176-absorbing-original-imafxynbchcfxdpj.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/ksru0sw0/short/i/g/q/xs-42500-urbanic-original-imag69t38kgmfrbu.jpeg?q=50"],
    "corset" : ["https://rukminim1.flixcart.com/image/495/594/ks6ef0w0/corset/o/c/u/l-cl10416-daluci-original-imag5ssnp4dcvn6n.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/jve4pe80/corset/j/v/u/l-cl10416-daluci-original-imafg8wwk88ptube.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/k3rmm4w0/shapewear/t/w/s/free-sfh000-shivaay-trading-co-original-imafgh4rhjmjdhte.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/l05lx8w0/shapewear/z/6/f/xxl-tummy-shapewear-hoopoes-original-imagcyc4af2kxng8.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/kmp7ngw0/corset/r/3/k/xl-po-2-xl-eleg-style-original-imagfjnxugszssv8.jpeg?q=50"],
    "peplumtop" : ["https://rukminim1.flixcart.com/image/495/594/kr3tj0w0/top/z/k/8/l-shirred-mizago-original-imag4zfhhzefz9yy.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/km6mxe80/top/n/y/d/xs-st01-silkova-original-imagf5fmh6gdecba.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/xif0q/top/1/n/9/l-black-001-dharam-fabrics-original-imaggdymqjgtye5r.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/kgy0sy80/top/f/m/j/s-bj-top375-hanumntra-original-imafx2zpfyghw8be.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/kjhgzgw0-0/top/e/q/o/m-bj-top377-hanumntra-original-imafzfgyvpgjty7y.jpeg?q=50"],
    "jumpsuit" : ["https://rukminim1.flixcart.com/image/495/594/kynb6vk0/jumpsuit/5/8/w/-original-imagattkcmgynfdt.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/ktizdzk0/jumpsuit/y/z/o/s-ss20an259jsc143-and-original-imag6ugvht4knube.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/k8ddoy80/jumpsuit/z/f/w/xxl-ss20at125jsdnm-and-original-imafqefgdgnks9z4.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/kynb6vk0/jumpsuit/n/j/b/-original-imagattkgahhqpq7.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/k6l2vm80/jumpsuit/z/f/u/xs-ss20an068jsrt-and-original-imafpycgpvgq5bju.jpeg?q=50"],
    "anarkalidress" : ["https://rukminim1.flixcart.com/image/495/594/kkyc9zk0/kurta/6/w/s/l-a-j-001-black-yesly-original-imagy6j2g7uxxkjg.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/kkyc9zk0/kurta/i/h/6/xl-a-j-001-yellwo-yesly-original-imagy6gpvgdaubcx.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/kmxsakw0/kurta/c/l/l/s-aj-517-aj-art-original-imagfqhc5bznnjhf.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/ku5ufm80/kurta/q/l/c/s-markr-002-blue-marwars-original-imag7cmnzzzy3gsn.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/kve530w0/kurta/l/7/q/xl-neemiya-blue-doongari-wala-original-imag8b5sprjzbqa4.jpeg?q=50"],
    "lehenga" : ["https://rukminim1.flixcart.com/image/495/594/l0y6qa80/kids-lehenga-choli/v/l/u/4-5-years-gajra-the-fashion-prime-original-imagcmgezfqsknry.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/kt7jv680/lehenga-choli/f/n/i/free-sleeveless-l8097-fashionuma-original-imag6hxffsx8hkgh.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/l2xmqvk0/lehenga-choli/a/x/m/free-sleeveless-l8097-anara-original-image5uvub9hh3hz.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/l20rma80/lehenga-choli/v/x/q/free-half-sleeve-jannat-black-r-h-comapany-original-imagdgzhznhnyttk.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/kwfaj680/lehenga-choli/o/g/s/free-half-sleeve-new-ruffle-designer-lehenga-cholis-for-indian-original-imag93xvfs2r6hbv.jpeg?q=50"],
    "maxidress" : ["https://rukminim1.flixcart.com/image/495/594/kqzj7gw0/dress/h/s/c/xl-shiv-607-shivam-creation-original-imag4vr4gthhpqxg.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/xif0q/dress/i/d/z/m-dv320-daevish-original-imag6fxn7fnrggra-bb.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/kvpklu80/dress/r/3/4/s-aa-0119-mauve-boho-long-dress-aayu-original-imag8k648mcxpeud.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/kvpklu80/dress/z/5/w/xl-aa-0119-blue-boho-long-dress-aayu-original-imag8k64fkkemmzc.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/k687wy80/dress/e/y/m/xl-270-dhvani-creation-original-imafnfd3cmshhhjy.jpeg?q=50"],
    "yogapants" : ["https://rukminim1.flixcart.com/image/495/594/kn7sdjk0/track-pant/b/q/g/28-awtp-21-anaghakart-original-imagfxz79gpe5v4k.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/kf4ajrk0/track-pant/e/v/g/m-1-17-yunek-original-imafvmpxsjerm4ye.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/kod858w0/track-pant/5/a/k/28-awtp-21-anaghakart-original-imag2ug84n4jxxd4.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/k30h8y80/track-pant/3/n/3/xs-m7-wm-t04-olive-m7-by-metronaut-original-imafk3v6ncya8hqu.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/k30h8y80/track-pant/v/q/j/xs-m7-wm-t02-pink-m7-by-metronaut-original-imafgyhdhvbfzsu6.jpeg?q=50"],
    "sherwani" : ["https://rukminim1.flixcart.com/image/495/594/kq6yefk0/sherwani/e/d/o/m-jss-7700007-chote-raja-collection-original-imag49fsunp9gkhw.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/l52sivk0/sherwani/d/8/h/m-jss-090707-chote-raja-collection-original-imagftcddba5eqfu.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/kq6yefk0/sherwani/1/x/x/l-jss-7700007-chote-raja-collection-original-imag49g3j9fqfaw8.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/kpcy5jk0/sherwani/5/w/d/xxl-mens-indo-western-25-n-b-f-fashion-original-imag3ma2kyhbvggm.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/kn0n6a80/sherwani/k/n/s/m-ol-golden147-phone-sg-rajasahab-original-imagfsjvd6vskhyn.jpeg?q=50"],
    "sequencedress" : ["https://rukminim1.flixcart.com/image/495/594/ku2zjww0/dress/e/s/m/l-1227-sheetal-associates-original-imag7aafnxemmm7x.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/ku2zjww0/dress/c/l/1/s-1143-sheetal-associates-original-imag7aa2fyu9cakg.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/l2m78280/dress/7/t/a/xl-bcl-seq-brucella-original-imagdwxfshsgs75h.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/l2m78280/dress/x/t/7/s-bcl-seq-brucella-original-imagdwxgdyr7qqbz.jpeg?q=50","https://rukminim1.flixcart.com/image/495/594/l2m78280/dress/f/g/s/l-bcl-seq-brucella-original-imagdwxfgatty4hz.jpeg?q=50"]
}

# path to the chromedriver.exe file
path = 'C:/Users/SUBHRAJIT/Downloads/chromedriver_win32/chromedriver.exe'

@app.route("/")
def home():
    return render_template("index.html", instaExtracted = "", facebExtracted = "", tweetExtracted = "")



@app.route("/instagram")
def instagram():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
    driver = webdriver.Chrome(path, options=options)


    driver.get("http://www.instagram.com")


    username = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
    password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))

    username.clear()
    username.send_keys("highdefinition137@gmail.com")
    password.clear()
    password.send_keys("HighDefinition123")

    button = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()

    time.sleep(5)

    string_to_be_deleted = ""
    kwrd = array_fashion

    for q_srch in range(0, len(kwrd)):

        curr = []

        keyword = kwrd[q_srch]
        driver.get("https://www.instagram.com/explore/tags/"+keyword[1:]+"/")
        n_scrolls = 1
        for j in range(0, n_scrolls):
            driver.execute_script("window.scrollTo(0, 0.01)")
            time.sleep(5)
        time.sleep(5)
        anchors = driver.find_elements(by=By.TAG_NAME, value="span")
        curr.append(keyword[1:])
        curr.append(anchors[3].text)
        curr.append("https://www.flipkart.com/search?q="+keyword[1:]+"&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off")
        insta.append(curr)

    instaExtracted = ""
    facebExtracted = ""
    tweetExtracted = ""
    if(len(insta) > 0):
        instaExtracted = "Extracted"

    if(len(faceb) > 0):
        facebExtracted = "Extracted"

    if(len(tweet) > 0):
        tweetExtracted = "Extracted"

    return render_template("index.html", instaExtracted = instaExtracted, facebExtracted = facebExtracted, tweetExtracted = tweetExtracted)





@app.route("/facebook")
def facebook():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")

    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications": 2}
    chrome_options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(path, options=options)
    driver.get("https://www.facebook.com/")

    username = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='email']")))
    password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='pass']")))

    username.clear()
    username.send_keys("highdefinition137@gmail.com")
    password.clear()
    password.send_keys("HighDefinition123")

    button = WebDriverWait(driver, 2).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()


    lists = array_fashion


    likes = []

    for keyword in lists:
        blank = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Search Facebook']")))
        length = len(blank.get_attribute('value'))
        blank.send_keys(length * Keys.BACKSPACE)

        blank.clear()
        val = keyword
        blank.send_keys(val)

        time.sleep(5)
        blank.send_keys(Keys.ENTER)
        time.sleep(5)

        el = driver.find_element(By.XPATH,
                                 "//span[@class='d2edcug0 hpfvmrgz qv66sw1b c1et5uql lr9zc1uh a8c37x1j fe6kdd0r mau55g9w c8b282yb keod5gw0 nxhoafnm aigsh9s9 d3f4x2em mdeji52x a5q79mjw g1cxx5fr b1v8xokw m9osqain hzawbc8m']").text
        curr = []
        curr.append(keyword[1:])
        curr.append(el[:5])
        curr.append("https://www.flipkart.com/search?q="+keyword+"&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off")
        faceb.append(curr)

    instaExtracted = ""
    facebExtracted = ""
    tweetExtracted = ""
    if(len(insta) != 0):
        instaExtracted = "Extracted"

    if(len(faceb) != 0):
        facebExtracted = "Extracted"

    if(len(tweet) != 0):
        tweetExtracted = "Extracted"

    return render_template("index.html", instaExtracted = instaExtracted, facebExtracted = facebExtracted, tweetExtracted = tweetExtracted)



@app.route('/twitter')
def twitter():
    api_key = "DSGTlJypHDP14hMvJwUpDSpIF"
    api_key_secret = "EBCVrQR1Dst2X5tMD2PpSa2qkGVmZyZFiWb2vkeClsgh6bj0BK"

    access_token = "1547872422640369664-y6QM9N0ehqX8IPfeYRvb8uD5kHXHSj"
    access_token_secret = "nzkhmGb5UKfZ5eOvLDXR79JCwG5kKRQioDBb9hRlYMj3d"

    bearer_token = "AAAAAAAAAAAAAAAAAAAAAAkJfAEAAAAAmWa%2BT8v6jNyIkwG5E2MbDzyEnMI%3DEYJp9mldQaf5TMrXbKjXOtXW5F8TpObgWMEYBgd4VQMQnQZJur"

    auth = tweepy.OAuthHandler(consumer_key=api_key, consumer_secret=api_key_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)
    print(api)
    queries = []
    for tag in array_fashion:
        queries.append(tag[1:] + " -is:retweet")
    for query in queries:
        client = tweepy.Client(bearer_token)
        counts = client.get_recent_tweets_count(query=query, granularity='day')

        sum = 0
        for i in counts.data:
            sum += (i["tweet_count"])

        curr = []
        x = query.split(" ")
        curr.append(x[0])
        curr.append(sum)
        curr.append("https://www.flipkart.com/search?q="+x[0]+"&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off")
        tweet.append(curr)

    instaExtracted = ""
    facebExtracted = ""
    tweetExtracted = ""
    if(len(insta) != 0):
        instaExtracted = "Extracted"

    if(len(faceb) != 0):
        facebExtracted = "Extracted"

    if(len(tweet) != 0):
        tweetExtracted = "Extracted"

    print(insta)
    print(faceb)
    print(tweet)

    return render_template("index.html", instaExtracted=instaExtracted, facebExtracted=facebExtracted,tweetExtracted=tweetExtracted)



@app.route('/fetch')
def fetch():
    p = len(insta)
    params = []
    for i in range (0,p):
        params.append(i)

    trends_facebook = []
    trends_insta = []
    trends_twitter = []

    for i in range (0, len(insta)):
        s = "0"
        for j in range (0, len(insta[i][1])):
            if(insta[i][1][j] == ','):
                continue
            s+=insta[i][1][j]
        trends_insta.append(int(s))


    for i in range (0, len(faceb)):
        faceb_number = faceb[i][1].split()[0]
        if(faceb_number[-1] == 'M'):
            face_num = faceb_number[0:len(faceb_number)-1]
            face_num = float(face_num)
            face_num = face_num * 100000
        elif(faceb_number[-1] == 'K'):
            face_num = faceb_number[0:len(faceb_number)-1]
            face_num = float(face_num)
            face_num = face_num * 1000
        else:
            face_num = faceb_number
            face_num = float(face_num)

        trends_facebook.append(face_num)

    for i in range (0, len(tweet)):
        tweet_num = int(tweet[i][1])
        trends_twitter.append(tweet_num)

    data = []
    data.append(trends_insta)
    data.append(trends_facebook)
    data.append(trends_twitter)
    data = [[data[j][i] for j in range(len(data))] for i in range(len(data[0]))]
    scaler_ = MinMaxScaler()
    df = pd.DataFrame(data, columns=['Instagram', 'Facebook', 'Twitter'])
    df = scaler_.fit_transform(df)
    trends_rank = []
    for i in range (0, len(df)):
        instagram_data = df[i][0]
        facebook_data = df[i][1]
        twitter_data = df[i][2]
        overall_data = (instagram_data*0.25) + (facebook_data*0.25) + (twitter_data*0.5)
        trends_rank.append([overall_data, array_fashion[i][1:],"https://www.flipkart.com/search?q="+array_fashion[i][1:]+"&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"])

    trends_rank.sort(reverse=True)
    print(trends_rank)

    return render_template("photo_div.html", trends_rank = trends_rank, array_fashion_images = array_fashion_images)



@app.route('/user',  methods = ['GET', 'POST'])
def user():
    try:
        if request.method == 'POST':
            user = request.form.get("url")
            trends = []
            '''
            Twitter
            '''
            api_key = "DSGTlJypHDP14hMvJwUpDSpIF"
            api_key_secret = "EBCVrQR1Dst2X5tMD2PpSa2qkGVmZyZFiWb2vkeClsgh6bj0BK"

            access_token = "1547872422640369664-y6QM9N0ehqX8IPfeYRvb8uD5kHXHSj"
            access_token_secret = "nzkhmGb5UKfZ5eOvLDXR79JCwG5kKRQioDBb9hRlYMj3d"

            bearer_token = "AAAAAAAAAAAAAAAAAAAAAAkJfAEAAAAAmWa%2BT8v6jNyIkwG5E2MbDzyEnMI%3DEYJp9mldQaf5TMrXbKjXOtXW5F8TpObgWMEYBgd4VQMQnQZJur"

            auth = tweepy.OAuthHandler(consumer_key=api_key, consumer_secret=api_key_secret)
            auth.set_access_token(access_token, access_token_secret)

            api = tweepy.API(auth)
            query = user + " -is:retweet"
            query = query[1:]
            print(query)
            client = tweepy.Client(bearer_token)
            counts = client.get_recent_tweets_count(query=query, granularity='day')
            sum = 0
            for i in counts.data:
                sum += (i["tweet_count"])

            trends.append(sum)

            options = webdriver.ChromeOptions()
            options.add_argument('headless')
            options.add_argument('window-size=1920x1080')
            options.add_argument("disable-gpu")

            '''
            Facebook
            '''
            driver = webdriver.Chrome(path, options=options)
            driver.get("https://www.facebook.com/")

            username = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='email']")))
            password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='pass']")))

            username.clear()
            username.send_keys("highdefinition137@gmail.com")
            password.clear()
            password.send_keys("HighDefinition123")

            button = WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()

            keyword = user

            blank = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Search Facebook']")))
            length = len(blank.get_attribute('value'))
            blank.send_keys(length * Keys.BACKSPACE)

            blank.clear()

            blank.send_keys(keyword)

            time.sleep(5)
            blank.send_keys(Keys.ENTER)
            time.sleep(5)

            el = driver.find_element(By.XPATH,
                                     "//span[@class='d2edcug0 hpfvmrgz qv66sw1b c1et5uql lr9zc1uh a8c37x1j fe6kdd0r mau55g9w c8b282yb keod5gw0 nxhoafnm aigsh9s9 d3f4x2em mdeji52x a5q79mjw g1cxx5fr b1v8xokw m9osqain hzawbc8m']").text
            trends.append(el[:4])

            '''INSTAGRAM'''
            curr = []
            driver = webdriver.Chrome(path, options=options)
            driver.get("http://www.instagram.com")

            username = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
            password = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))

            username.clear()
            username.send_keys("highdefinition137@gmail.com")
            password.clear()
            password.send_keys("HighDefinition123")

            button = WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()

            time.sleep(5)
            string_to_be_deleted = ""
            searchbox = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Search']")))
            searchbox.clear()

            keyword = user
            l = len(string_to_be_deleted[1:])
            i = 0
            while (i <= l):
                searchbox.send_keys(Keys.BACK_SPACE)
                i += 1

            string_to_be_deleted = keyword
            searchbox.send_keys(keyword)

            time.sleep(5)
            my_link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/" + keyword[1:] + "/')]")))
            my_link.click()

            n_scrolls = 1
            for j in range(0, n_scrolls):
                driver.execute_script("window.scrollTo(0, 0.01)")
                time.sleep(5)

            anchors = driver.find_elements(by=By.TAG_NAME, value="span")
            curr.append(keyword[1:])
            curr.append(anchors[3].text)
            curr.append("https://www.flipkart.com/search?q=" + keyword[1:] + "&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off")
            trends.append(anchors[3].text)


            driver.get("https://www.flipkart.com/search?q="+user[1:]+"&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off")
            anch = driver.find_elements(by=By.CLASS_NAME, value="_2r_T1I")
            image_ans = []
            for a in anch:
                image_ans.append(a.get_attribute("src"))

            print(image_ans)
            for i in trends:
                print(i)
        trends[1] = trends[1].split()[0]
        user_text = user[1:]
        user_link = "https://www.flipkart.com/search?q="+user_text+"&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"
    except NoSuchElementException:
        return render_template("index_error.html")
    return render_template("display_user.html", trends = trends, user_link = user_link, user_text = user_text, image_ans = image_ans)




app.run(debug=True)