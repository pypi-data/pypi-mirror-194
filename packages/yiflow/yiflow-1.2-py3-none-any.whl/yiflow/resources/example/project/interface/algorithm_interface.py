import yiflow as yf
 
 
class AlgorithmInterface(yf.Interface):

    def __init__(self, config_file=None, **kwargs):
        super().__init__(config_file, **kwargs)

    # Name of methods can be customized
    def run(self, req):
        image_name = req['imageName']
        image_data = req['imageData']

        feed_dict = dict(
            image=image_data
        )

        # Do whatever you want with flows
        self.flow1(feed_dict)
        # self.flow2(feed_dict)

        # Construct response
        resp = {}
        resp['image_path'] = image_name
        resp['alarm'] = feed_dict['alarm']
        if 'drawed' in feed_dict:
            resp['drawed'] = feed_dict['drawed']

        return resp
