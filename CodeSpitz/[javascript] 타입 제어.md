# [javascript] νμ μ μ΄

<aside>
π ν¨μ μμ€μμ κ°νμ μ μ΄λ₯Ό μ μΈνμ¬λ³΄κ³  νμ€νΈ νλ€.

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
#μκ·Έλμ² μ μΈκ³Ό λμμ νμ μ²΄ν¬κ° κ°λ₯νλ€.
#μ΄λ κ² ν¨μλ₯Ό μ§λμΌλ©΄ νμ μ μ΄λ‘ !== , === νλΉκ΅ μ°μ°μλ₯Ό μ¬μ© ν  νμκ° μλ€.
#μΈμ΄μ λν κΉμ μ΄ν΄κ° κΈ°λ°, μλ°μ€ν¬λ¦½νΈλ λνΉν μΈμ΄.
```