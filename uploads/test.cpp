#include<iostream>
using​​namespace​​std​;int​​findSecondLargest​(​int​​arr​[​10​],​int​​size​){​int​​second​;​for​ (​int​​i​​=​​0​; ​i​​<​​size​; ​i​++​)    // Last i elements are already in place​for​ (​int​​j​​=​​0​; ​j​​<​​size​-​i​-​1​; ​j​++​)​if​ (​arr​[​j​] ​>​​arr​[​j​+​1​]){​int​​t​;​t​​=​​arr​[​j​];​arr​[​j​] ​=​​arr​[​j​+​1​];​arr​[​j​+​1​] ​=​​t​;        }​second​​=​​arr​[​size​-​2​];​return​​second​;}int​​main​(){​int​​arr​[​10​];​int​​size​​=​​10​;​cout​​<<​​"Enter 10 array elements:"​;​for​(​int​​i​=​0​;​i​<​10​;​i​++​){​cin​>>​arr​[​i​];    }​cout​​<<​"Second largest number : "​<<​​findSecondLargest​(​arr​,​size​);}