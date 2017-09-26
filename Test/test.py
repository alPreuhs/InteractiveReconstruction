def radonRayDrivenApproach(img, img_interp_spline, dSI, dDI, val, detectorSize, detectorSpacing, numProj):
    # debugging arrays for showing the source positions
    source_pos_x_list = []
    source_pos_y_list = []
    # debugging arrays for showing the piercing positions
    piercing_x = []
    piercing_y = []
    # debugging arrays for showing the piercing positions
    cur_x = []
    cur_y = []

    # Defining the fanogram image
    fanogram = Image.new(img.mode, (377, 377))  # create a new black image
    pixels = fanogram.load()

    ##calculate index for detector pixels
    detectorSizeIndex = (detectorSize / detectorSpacing)
    ## calculate fan angle
    gammaM = math.atan((detectorSize / 2.0 - 0.5) / dSI)
    ## calculate scanning range which is 180+fan angle (short scan)
    angRange = math.pi + 2 * gammaM
    ## calculate angular step size
    angStepSize = angRange / numProj
    maxBetaIndex = (int)(angRange / angStepSize)
    print(maxBetaIndex)

    # iterate over the rotation angle
    for angle_index in range(0, 5):

        # calculate actual angle which are distributed equally over short scan range + 180 degree shift...
        beta = angStepSize * angle_index + math.pi / 2
        # beta = val - gammaM
        # print(beta)

        # calculate cos/sin
        cosBeta = math.cos(beta)
        sinBeta = math.sin(beta)

        # compute source position
        source_x = dSI * (cosBeta)
        source_y = dSI * sinBeta
        source_position = (source_x, source_y)
        # compute piercing point
        PP_Point_x = -detectorSize / 2 * sinBeta
        PP_Point_y = detectorSize / 2 * cosBeta
        PP = (PP_Point_x, PP_Point_y)
        # print(source_position)
        # print(PP)

        # calculate direction orthogonal to central ray -> pointing parallel to detector
        v = np.array(PP) * np.array([-1])
        ortho_direction = np.linalg.norm(v)
        ortho_direction = v / ortho_direction
        # print(ortho_direction)

        ### add values for debugging
        source_pos_x_list.append(source_x)
        source_pos_y_list.append(source_y)
        piercing_x.append(PP_Point_x)
        piercing_y.append(PP_Point_y)

        # iterate over detector elements
        for t in range(0, int(detectorSizeIndex)):
            stepsDirection = 0.5 * detectorSpacing + t * detectorSpacing
            ##shift detector indices
            # t = detectorSizeIndex*0.5

            ## calculate world point for current pixel
            pixel_position = np.array(PP, dtype=Decimal) + (np.array(stepsDirection * ortho_direction, dtype=Decimal))
            # print(pixel_position)

            ## calculate distence between source position and detector pixel
            distance = np.linalg.norm(
                np.array(pixel_position, dtype=Decimal) - np.array(source_position, dtype=Decimal), ord=2)
            # print(distance)
            # Define increment step
            increment = 0.5
            sum = 0.0
            height, width = img.size

            # integral along the line

            # Define maximal distance index
            max_distance_index = int(distance / increment)
            for line_index in np.arange(0, max_distance_index):
                current = np.array(source_position, dtype=Decimal) + increment * line_index
                current = np.array(current)

                X_Image = current.item(0)
                Y_Image = current.item(1)
                cur_x.append(X_Image)
                cur_y.append(Y_Image)

                # print(X_Image,Y_Image)
                # print("current      ", current)
                # sum = interpolate.Rbf(current.item(0),current.item(1),arr,function='linear

                fanogram = img_interp_spline(X_Image, Y_Image)
                # sum += interp1d(current.item(0),current.item(1),"linear")
                # print(pixels[angle_index, t] )
                # print("sum    ", sum)

    # plt.plot(source_pos_x_list, source_pos_y_list)
    # plt.show()
    plt.plot(source_pos_x_list, source_pos_y_list, 'rx')
    # plt.plot(cur_x, cur_y, 'gx')
    plt.plot(piercing_x, piercing_y, 'bo')
    plt.show()
    return fanogram

