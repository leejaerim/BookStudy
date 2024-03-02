# [builder 패턴]

- 객체 리터럴이나, 생성자(오버로딩)을 통한 객체 생성은 파라미터의 종류와 값에 따라 무한히 늘어날 수 있다.
- 이와 반면에 자바빈객체의 경우 setter메소드를 통해 객체값을 설정할 수 있다.
- 이 두가지의 장점을 합친 패턴이 빌더 패턴이라고 볼수 있다.
- 예제 코드를 보며 분석하도록 하자.

```java
public class Computer {
	
    //required parameters
    private String HDD;
    private String RAM;
	
    //optional parameters
    private boolean isGraphicsCardEnabled;
    private boolean isBluetoothEnabled;
	
 
    public String getHDD() {
        return HDD;
    }
 
    public String getRAM() {
        return RAM;
    }
 
    public boolean isGraphicsCardEnabled() {
        return isGraphicsCardEnabled;
    }
 
    public boolean isBluetoothEnabled() {
        return isBluetoothEnabled;
    }
	
    private Computer(ComputerBuilder builder) {
        this.HDD=builder.HDD;
        this.RAM=builder.RAM;
        this.isGraphicsCardEnabled=builder.isGraphicsCardEnabled;
        this.isBluetoothEnabled=builder.isBluetoothEnabled;
    }
	
    //Builder Class
    public static class ComputerBuilder{
 
        // required parameters
        private String HDD;
        private String RAM;
 
        // optional parameters
        private boolean isGraphicsCardEnabled;
        private boolean isBluetoothEnabled;
		
        public ComputerBuilder(String hdd, String ram){
            this.HDD=hdd;
            this.RAM=ram;
        }
 
        public ComputerBuilder setGraphicsCardEnabled(boolean isGraphicsCardEnabled) {
            this.isGraphicsCardEnabled = isGraphicsCardEnabled;
            return this;
        }
 
        public ComputerBuilder setBluetoothEnabled(boolean isBluetoothEnabled) {
            this.isBluetoothEnabled = isBluetoothEnabled;
            return this;
        }
		
        public Computer build(){
            return new Computer(this);
        }
 
    }
 
}
```

- 가장 중요한 것은, builder 클래스를 이용하여 인스턴스를 생성하는 부분은 private로 은닉화 되어  있다.(public 생성자가 없어 해당 클래스의 인스턴스를 생성하려면 builder클래스를 꼭 거쳐야한다.) 또, set함수 없이 , get함수만 존재한다.
- 메인함수는 다음과 같다.
    
    ```java
    public class TestBuilderPattern {
     
        public static void main(String[] args) {
            Computer comp = new Computer.ComputerBuilder("500 GB", "2 GB")
                    .setBluetoothEnabled(true)
                    .setGraphicsCardEnabled(true)
                    .build();
        }
     
    }
    ```
    
- 필수값은 파라미터로 부여받으며, 옵션값은 setter함수를 통해 입력받는다.
- builder 클래스의 옵션메소드 리턴값은 this, 즉 자기자신이여야 한다.