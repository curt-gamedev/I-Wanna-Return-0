<?xml version="1.0" encoding="UTF-8"?>
<tileset version="1.10" tiledversion="1.12.2" name="killers" tilewidth="32" tileheight="32" tilecount="10" columns="0">
 <grid orientation="orthogonal" width="1" height="1"/>
 <tile id="0">
  <image source="../Cherry_0.png" width="21" height="24"/>
 </tile>
 <tile id="1">
  <properties>
   <property name="direction" value="down"/>
  </properties>
  <image source="../SpikeDown.png" width="32" height="32"/>
  <objectgroup draworder="index" id="2">
   <object id="1" x="0" y="0">
    <polygon points="0,0 16,32 32,0"/>
   </object>
  </objectgroup>
 </tile>
 <tile id="9">
  <image source="../SpikeDown.png" width="32" height="32"/>
  <objectgroup draworder="index" id="2">
   <object id="1" x="1" y="0">
    <polygon points="0,0 30,0 30,2 15,32 0,2"/>
   </object>
  </objectgroup>
 </tile>
 <tile id="2">
  <properties>
   <property name="direction" value="left"/>
  </properties>
  <image source="../SpikeLeft.png" width="32" height="32"/>
  <objectgroup draworder="index" id="2">
   <object id="1" x="32" y="32">
    <polygon points="0,0 -32,-16 0,-32"/>
   </object>
  </objectgroup>
 </tile>
 <tile id="3">
  <properties>
   <property name="direction" value="right"/>
  </properties>
  <image source="../SpikeRight.png" width="32" height="32"/>
  <objectgroup draworder="index" id="2">
   <object id="1" x="0" y="0">
    <polygon points="0,0 32,16 0,32"/>
   </object>
  </objectgroup>
 </tile>
 <tile id="4">
  <properties>
   <property name="direction" value="up"/>
  </properties>
  <image source="../SpikeUp.png" width="32" height="32"/>
  <objectgroup draworder="index" id="2">
   <object id="1" x="0" y="32">
    <polygon points="0,0 16,-32 32,0"/>
   </object>
  </objectgroup>
 </tile>
 <tile id="5">
  <image source="../MiniSpike-Up.png" width="16" height="16"/>
  <objectgroup draworder="index" id="2">
   <object id="2" x="0" y="16">
    <polygon points="0,0 8,-16 16,0"/>
   </object>
  </objectgroup>
 </tile>
 <tile id="6">
  <image source="../MiniSpike-Right.png" width="16" height="16"/>
  <objectgroup draworder="index" id="2">
   <object id="1" x="0" y="0">
    <polygon points="0,0 16,8 0,16"/>
   </object>
  </objectgroup>
 </tile>
 <tile id="7">
  <image source="../MiniSpike-Left.png" width="16" height="16"/>
  <objectgroup draworder="index" id="2">
   <object id="1" x="16" y="16">
    <polygon points="0,0 -16,-8 0,-16"/>
   </object>
  </objectgroup>
 </tile>
 <tile id="8">
  <image source="../MiniSpike-Down.png" width="16" height="16"/>
  <objectgroup draworder="index" id="2">
   <object id="1" x="0" y="0">
    <polygon points="0,0 8,16 16,0"/>
   </object>
  </objectgroup>
 </tile>
</tileset>
