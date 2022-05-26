# [javascript] 타입 제어

<aside>
📌 함수 수준에서 강타입 제어를 선언하여보고 테스트 한다.

</aside>

```jsx
const type = (target,type)=>{
    if(typeof type == "string"){
        if(typeof target != type) throw `invalid ${target} : ${type}`;
    }
    else if(!(target instanceof type)) throw `invalid type ${target} : ${type}`;
    return target;
};
```

```jsx
const test(target, _=type(target,'string'))=>(){
}
#시그니처 선언과 동시에 타입 체크가 가능하다.
#이렇게 함수를 짜놓으면 타입 제어로 !== , === 형비교 연산자를 사용 할 필요가 없다.
#언어에 대한 깊은 이해가 기반, 자바스크립트는 독특한 언어.
```