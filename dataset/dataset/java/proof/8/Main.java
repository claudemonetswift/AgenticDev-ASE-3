//A simple representation of the location from the source code in regards to the question asked.

//Runs two versions of the code on two sets of devices and views. One which uses a global orientation
//variable to check whether it should configure the device to the view when the configuration of the view changes 
//or not, and one which does so any time the configuration of the view changes.
public class Main {
    public static Device androidPhone = new Device(390, 844, "HORIZONTAL"); //Representation of the device
                                                                                    //In the fixed code.
    public static Device androidPhoneOnlyGlobal = new Device(390, 844, "HORIZONTAL");
                                                                                    //Representation of the device
                                                                                    //In the broken code.
    public static String globalOrientation = "HORIZONTAL"; //The global orientation. Only used in the broken code.

    //The test.
    public static void main(String[] args) {
        ImageView newConfig = new ImageView(390, 844, "HORIZONTAL"); //Representative of the view in the
                                                                            //fixed code.
        ImageView newConfigOnlyGlobal = new ImageView(390, 844, "HORIZONTAL"); //Representative of the view
                                                                                       //In the broken code.
        //Initalization state. Uses configureForOrientation() so that the views and the devices are the same.
        androidPhone.configureForOrientation(newConfig);
        androidPhoneOnlyGlobal.configureForOrientation(newConfigOnlyGlobal);

        //Tests will return false for any discrepencies between a view and its corrosponding device, and
        //true if their configurations match.

        //Runs fine for both
        System.out.println("Initalization case: ");
        System.out.println("    Fixed code:");
        System.out.println(androidPhone.matchesView(newConfig));
        System.out.println("    Broken code:");
        System.out.println(androidPhoneOnlyGlobal.matchesView(newConfigOnlyGlobal));

        //Runs fine for both.
        System.out.println("\nOrientation change case: ");
        OnConfigurationChanged(newConfig, newConfigOnlyGlobal, 390, 844, "VERTICAL");

        //Fails for the broken code.
        System.out.println("\nSize change case: ");
        OnConfigurationChanged(newConfig, newConfigOnlyGlobal, 400, 850, "VERTICAL");

        //Could add more tests, but I fail to see the point of more rigourous testing on
        //such a simple representation of the Android Java API for such an obvious
        //fix to the error. Especially one which is used in the code of the current final product.

    }

    //Represents OnConfigurationChanged. In the source code, runs whenever the view's configuration changes.
    static void OnConfigurationChanged(ImageView newConfig, ImageView newConfigOnlyGlobal, int h, int w, String o) {
        System.out.println("Running OnConfigurationChanged()... ");

        //Simulating the changes to the view's configuration which would cause
        //OnConfiguration to run in the source code.
        newConfig.setHeight(h);
        newConfig.setWidth(w);
        newConfig.setOrientation(o);
        newConfigOnlyGlobal.setHeight(h);
        newConfigOnlyGlobal.setWidth(w);
        newConfigOnlyGlobal.setOrientation(o);

        //A representation of the code which was the subject of the question.
        if (!(globalOrientation.equals(newConfigOnlyGlobal.getOrientation()))) {
            globalOrientation = newConfigOnlyGlobal.getOrientation();
            //Broken code:
            androidPhoneOnlyGlobal.configureForOrientation(newConfigOnlyGlobal);
        }
        //Fixed code:
        androidPhone.configureForOrientation(newConfig);

        //Output
        System.out.println("    Fixed code:");
        System.out.println(androidPhone.matchesView(newConfig));
        System.out.println("    Broken code:");
        System.out.println(androidPhoneOnlyGlobal.matchesView(newConfigOnlyGlobal));
    }
}

