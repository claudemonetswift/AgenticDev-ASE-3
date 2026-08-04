//Represents a view's configuration, including its width, height, and orientation.
class ImageView {
    private int width;
    private int height;
    private String orientation;

    public ImageView(int w, int h, String o) {
      this.width = w;
      this.height = h;
      this.orientation = o;
    }

    public int getWidth() {
        return this.width;
    }

    public int getHeight() {
        return this.height;
    }

    public String getOrientation() {
        return this.orientation;
    }

    public void setWidth(int w) {
        this.width = w;
    }

    public void setHeight(int h) {
        this.height = h;
    }

    public void setOrientation(String o) {
        this.orientation = o;
    }

    
}
