//Represents a device's configuration, including its width, size, and orientation.
public class Device {
    int width;
    int height;
    String orientation;

    public Device(int w, int h, String o) {
      this.width = w;
      this.height = h;
      this.orientation = o;
    }

    //Representation of configureForOrientation.
    //Changes the device's configuration to match the configuration of a given view.
    public void configureForOrientation(ImageView newConfig) {
        if (newConfig.getOrientation().equals("VERTICAL")) {
            this.orientation = "VERTICAL";
            this.height = newConfig.getHeight();
            this.width = newConfig.getWidth();
        } else {
            this.orientation = "HORIZONTAL";
            this.width = newConfig.getHeight();
            this.height = newConfig.getWidth();
        }
    }

    //Unique to the proof, used to check for errors.
    //Compares a view to the device. If there is a discrepency, retruns false. Otherwise, returns true.
    public boolean matchesView(ImageView newConfig) {
        boolean returnValue = true;
        if (!(this.orientation.equals(newConfig.getOrientation()))) {
            System.out.println("Orientation was not consistent between the device and the view.");
            returnValue = false;
        }
        if (this.orientation.equals("HORIZONTAL")) {
            if (!(this.height == newConfig.getWidth())) {
                System.out.println("Height was not consistent between the device and the view.");
                returnValue = false;
            }
            if (!(this.width == newConfig.getHeight())) {
                System.out.println("Width was not consistent between the device and the view.");
                returnValue = false;
            }
        } else {
            if (!(this.height == newConfig.getHeight())) {
                System.out.println("Height was not consistent between the device and the view.");
                returnValue = false;
            }
            if (!(this.width == newConfig.getWidth())) {
                System.out.println("Width was not consistent between the device and the view.");
                returnValue = false;
            }
        }

        return returnValue;
    }
}
